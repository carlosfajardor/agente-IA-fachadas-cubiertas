import langgraph
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader

# Configurar modelo de IA
llm = ChatOpenAI(model="gpt-4")

# Cargar documentos de normativa
loader = DirectoryLoader("data", glob="*.pdf")
docs = loader.load()

# Crear base de conocimiento vectorial
vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())

def buscar_respuesta(input_text):
    resultados = vectorstore.similarity_search(input_text, k=3)
    contexto = "\n".join([r.page_content for r in resultados])
    return llm.predict(f"Usando esta información:\n{contexto}\nResponde la pregunta: {input_text}")

def identificar_tipo_pregunta(input_text):
    if "ley" in input_text or "garantía" in input_text:
        return "consulta_juridica"
    elif "humedad" in input_text or "fisura" in input_text:
        return "consulta_tecnica"
    elif "constructora no responde" in input_text:
        return "respuesta_PQR"
    else:
        return "consulta_general"

def generar_respuesta_PQR(input_text):
    return llm.predict("Genera una respuesta formal para responder a la constructora: " + input_text)

graph = langgraph.Graph()
graph.add_node("consulta_tecnica", buscar_respuesta)
graph.add_node("consulta_juridica", buscar_respuesta)
graph.add_node("respuesta_PQR", generar_respuesta_PQR)
graph.add_node("consulta_general", llm)

graph.add_edge("consulta_tecnica", "output")
graph.add_edge("consulta_juridica", "output")
graph.add_edge("respuesta_PQR", "output")
graph.add_edge("consulta_general", "output")

def procesar_pregunta(pregunta):
    tipo = identificar_tipo_pregunta(pregunta)
    return graph.run(tipo, pregunta)
