import chromadb
from chromadb.utils import embedding_functions
from dotenv import dotenv_values
from jproperties import Properties


def connect_to_database(ip: str, port:int) -> chromadb.ClientAPI:
    db = chromadb.HttpClient(host=ip, port=port)
    return db

def getEmbeddingFunc():  
    props = Properties()
    with open('model.properties', 'rb') as file:
        props.load(file)
        props = props.properties
    if props["useOpenAI"] == "True":
        return getOpenAIEmbeddingFunc()
    return huggingFaceEmbeddingFunc(props)


def getOpenAIEmbeddingFunc():
    api_key = dotenv_values('./.env')["OPENAI_API_KEY"] 
    return embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-ada-002"
    )

def huggingFaceEmbeddingFunc(props: dict):
    api_key = dotenv_values('./.env')["HUGGINGFACE_API_KEY"]
    return embedding_functions.HuggingFaceEmbeddingFunction(
        api_key=api_key,
        model_name=props["huggingFaceEmbeddingModel"]
    )
