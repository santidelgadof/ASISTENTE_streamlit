from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import os
import streamlit as st
from pandasai.responses.response_parser import ResponseParser

# Inicializar PandasAI con OpenAI (u otro LLM si tienes uno local)
llm = OpenAI(api_token=os.getenv("OPENAI_API_KEY"))

class StreamlitResponse(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def format_dataframe(self, result):
        st.dataframe(result["value"])
        return

    def format_plot(self, result):
        st.image(result["value"])
        return

    def format_other(self, result):
        st.write(result["value"])
        return
    
# Función para realizar la consulta usando SmartDataframe
def query_smart_dataframe(prompt, df):
    smart_df = SmartDataframe(df, config={'llm': llm,
                                          "response_parser": StreamlitResponse})
    try:
        response = smart_df.chat(prompt)
        return response
    except UnicodeDecodeError as e:
        return f"Error de codificación: {str(e)}"
    except ValueError as e:
        return f"Error en el valor proporcionado: {str(e)}"
    except KeyError as e:
        return f"Error: La clave {str(e)} no existe en el contexto."
    except Exception as e:
        return f"Error inesperado: {str(e)}"


# Nueva función con un prompt mejorado
def enhanced_query_smart_dataframe(prompt, df, context):
    structured_prompt = f"Con el siguiente contexto: {context}. {prompt}"
    return query_smart_dataframe(structured_prompt, df)
