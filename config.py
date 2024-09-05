from sqlalchemy import create_engine, text
import streamlit as st
import pymysql

# Configuración de la conexión a la base de datos
def get_db_engine():
    engine = create_engine(
        f"mysql+pymysql://{st.secrets['DB_USER']}:{st.secrets['DB_PASSWORD']}@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}",
        connect_args={'charset': 'utf8mb4'},
        echo=False
    )
    return engine

# Función para ejecutar una consulta
def run_query(query):
    engine = get_db_engine()
    with engine.connect() as connection:
        result = connection.execute(text(query))  # Usar `text()` para escribir consultas SQL
        return result.fetchall()
