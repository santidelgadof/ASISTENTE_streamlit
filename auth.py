import hashlib
import os

# Función para hashear la contraseña con sal
def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16).hex()  # Generar una sal única
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_password, salt

# Función para autenticar usuarios utilizando el hash y la sal
def authenticate_user(email, password, user_data):
    user = user_data[user_data['email'] == email]
    if not user.empty:
        stored_salt = user.iloc[0]['salt']  # Recuperar la sal almacenada
        hashed_password, _ = hash_password(password, salt=stored_salt)
        if hashed_password == user.iloc[0]['contraseña']:
            return user.iloc[0]
    return None
