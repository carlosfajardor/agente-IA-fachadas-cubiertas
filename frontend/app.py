import streamlit as st
import requests

st.title("Agente de Consultoría en Fachadas y Cubiertas")

pregunta = st.text_input("Escribe tu consulta:")

if st.button("Consultar"):
    respuesta = requests.post("http://127.0.0.1:8000/consultar", json={"pregunta": pregunta}).json()
    st.write("Respuesta:", respuesta["respuesta"])
