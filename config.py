from sqlalchemy import create_engine
import pymysql

# Configuración de la conexión a la base de datos
def get_db_engine():
    engine = create_engine(
        f"mysql+pymysql://{st.secrets['DB_USER']}:{st.secrets['DB_PASSWORD']}@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}",
        connect_args={'charset': 'utf8mb4'},  # Mantén el charset si es necesario
        echo=False
    )
    return engine
