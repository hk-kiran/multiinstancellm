import chromadb
from chromadb.utils import embedding_functions
from dotenv import dotenv_values

def connect_to_database(ip: str, port:int) -> chromadb.ClientAPI:
    db = chromadb.HttpClient(host=ip, port=port)
    return db



def getOpenAIEmbeddingFunc():
    api_key = dotenv_values('./.env')["OPENAI_API_KEY"] 
    return embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-ada-002"
    )


