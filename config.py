import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargar las variables de entorno desde mysql.env
load_dotenv("mysql.env")

# Configurar la conexión a la base de datos MySQL usando SQLAlchemy
def get_db_engine():
    engine = create_engine(
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
        connect_args={'charset': 'utf8mb4'},  # Usar utf8mb4 para mejor compatibilidad con caracteres especiales
        encoding='utf-8',
        echo=False
    )
    return engine
