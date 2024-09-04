import pandas as pd
import hashlib
import os

def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16).hex()
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_password, salt


def authenticate_user(email, password, user_data):
    hashed_password = hash_password(password)
    user = user_data[(user_data['email'] == email) & (user_data['contraseña'] == hashed_password)]
    if not user.empty:
        return user.iloc[0]
    else:
        return None
