import base64

# Abre el archivo Excel que contiene las contraseñas
with open("DOC/database.xlsx", "rb") as f:
    # Codifica el archivo en base64
    encoded_excel = base64.b64encode(f.read()).decode("utf-8")

# Guarda la cadena base64 en un archivo de texto para usarla en Streamlit secrets
with open("encoded_excel.txt", "w") as text_file:
    text_file.write(encoded_excel)
