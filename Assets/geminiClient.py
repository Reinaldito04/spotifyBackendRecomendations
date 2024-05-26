
import google.generativeai as genAi
from dotenv import load_dotenv
import os

load_dotenv()

API= os.getenv('GeminiApiKey')


class GeminiAi:
    def Question(self, pregunta: str, canciones: list):
        
        modelo = genAi.GenerativeModel('gemini-pro')
        genAi.configure(api_key=API)
        pregunta_procesada = pregunta + " Recomiendo las siguientes canciones: " + ", ".join(canciones)
        pregunta =modelo.generate_content(pregunta_procesada)
        respuesta = pregunta.text   
        respuestaFiltrada = respuesta.replace('*','')   
        return respuestaFiltrada
