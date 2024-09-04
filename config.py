import streamlit as st
from sqlalchemy import create_engine

# Configurar la conexión a la base de datos MySQL usando las variables de Streamlit Secrets
def get_db_engine():
    engine = create_engine(
        f"mysql+pymysql://{st.secrets['DB_USER']}:{st.secrets['DB_PASSWORD']}@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}",
        connect_args={'charset': 'utf8mb4'},  # Usar utf8mb4 para mejor compatibilidad con caracteres especiales
        encoding='utf-8',
        echo=False
    )
    return engine
