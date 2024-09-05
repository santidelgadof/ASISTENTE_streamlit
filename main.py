import streamlit as st
import pandas as pd
import os
from io import BytesIO
import base64
from data_loader import load_topics, save_topic, delete_topic
from query_executor import enhanced_query_smart_dataframe
from config import get_db_engine
from auth import hash_password

# Obtener el archivo codificado en base64 desde st.secrets
encoded_excel = st.secrets["passwords_excel"]

# Decodificar el archivo y leerlo como un DataFrame de pandas
decoded_excel = base64.b64decode(encoded_excel)
df = pd.read_excel(BytesIO(decoded_excel))

# Función para autenticar usuario
def authenticate_user(email, password, df):
    # Buscar en el DataFrame el usuario y su contraseña hasheada
    hashed_password, _ = hash_password(password)
    user = df[(df['email'] == email) & (df['contraseña'] == hashed_password)]

    if not user.empty:
        return True
    else:
        return False


# Crear la carpeta para guardar datos de usuario si no existe
if not os.path.exists('user_data'):
    os.makedirs('user_data')

# Modo avanzado solo para administradores
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['user'] = None

if not st.session_state['authenticated']:
    st.title("Login:")
    email = st.text_input("Correo Electrónico")
    password = st.text_input("Contraseña", type="password")

    if st.button("Login"):
        user = authenticate_user(email, password, df)
        if user is not None:
            st.session_state['authenticated'] = True
            st.session_state['user'] = user
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
else:
    user = st.session_state['user']
    st.sidebar.title(f"Usuario: {user['nombre']} ({user['rol']})")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.clear()
        st.rerun()

    # Modo avanzado solo para administradores
    advanced_option = False
    if user['rol'] == 'admin':
        st.sidebar.subheader("Opciones Avanzadas")
        advanced_option = st.sidebar.checkbox("Modo Avanzado")

    # Modo avanzado: gestión de temas para administradores
    if advanced_option and user['rol'] == 'admin':
        st.title("Modo Avanzado: Gestión de Temas")

        # Entrada para crear un nuevo tema
        new_topic = st.text_input("Nuevo Tema")
        description = st.text_area("Descripción del tema")
        sql_query = st.text_area("Consulta SQL del tema")

        if st.button("Guardar Tema"):
            if new_topic and description and sql_query:
                save_topic(new_topic, description, sql_query, user['nombre'])
                st.success(f"Tema '{new_topic}' guardado con éxito.")
            else:
                st.error("Debe proporcionar un nombre, una descripción y una consulta SQL.")

        # Mostrar y permitir eliminar temas
        st.subheader("Temas guardados")
        topics = load_topics()
        if topics:
            for topic_name, details in topics.items():
                st.write(f"{topic_name}: (Creado por {details['creator']})")
                if details['creator'] == user['nombre'] and st.button(f"Eliminar {topic_name}"):
                    delete_topic(topic_name, user['nombre'])
                    st.success(f"Tema '{topic_name}' eliminado.")
        else:
            st.info("No hay temas guardados.")

    # Parte simple para viewers y admins: consulta de temas guardados
    else:
        st.title("Asistente Netex: Consultas Inteligentes")

        # Obtener los temas guardados
        topics = load_topics()

        if topics:
            # Recuperar el último tema seleccionado desde la sesión, si existe
            tema_previamente_seleccionado = st.session_state.get('last_selected_topic', "")

            # Seleccionar el tema desde el selectbox
            tema = st.selectbox(
                "Selecciona el tema:",
                [""] + list(topics.keys()), index=([""] + list(topics.keys())).index(tema_previamente_seleccionado) if tema_previamente_seleccionado in topics else 0
            )

            # Si se selecciona un nuevo tema, guardarlo en la sesión
            if tema:
                st.session_state['last_selected_topic'] = tema

                st.write(topics[tema]['description'])

                # Ejecutar la consulta SQL del tema guardado
                sql_query = topics[tema]['sql_query']
                if "sql_df" not in st.session_state or st.session_state.get('last_sql_query') != sql_query:
                    if st.button("Cargar Datos"):
                        try:
                            with st.spinner("Ejecutando consulta SQL del tema..."):
                                engine = get_db_engine()
                                df = pd.read_sql(sql_query, engine)

                                if df.empty:
                                    st.warning("La consulta no devolvió resultados.")
                                else:
                                    st.success("Consulta ejecutada exitosamente.")
                                    st.session_state['sql_df'] = df
                                    st.session_state['last_sql_query'] = sql_query
                        except Exception as e:
                            st.error(f"Error al ejecutar la consulta: {str(e)}")

                # Si ya se ha ejecutado la consulta SQL
                if 'sql_df' in st.session_state:
                    # Mostrar los datos y permitir preguntas según el rol del usuario
                    prompt = st.text_input("Pregunta sobre los datos obtenidos:")
                    
                    if st.button("Generar Respuesta") and prompt:
                        with st.spinner("Generando respuesta..."):
                            response = enhanced_query_smart_dataframe(prompt, st.session_state['sql_df'], topics[tema]['description'])
                            st.write("Respuesta:", response)
        else:
            st.info("No hay temas disponibles.")