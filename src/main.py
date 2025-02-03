from fastapi import FastAPI
from pydantic import BaseModel
from src.chatbot import procesar_pregunta

app = FastAPI()

class Consulta(BaseModel):
    pregunta: str

@app.post("/consultar")
def consultar(consulta: Consulta):
    respuesta = procesar_pregunta(consulta.pregunta)
    return {"respuesta": respuesta}
