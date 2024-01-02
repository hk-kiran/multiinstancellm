from llama_index import VectorStoreIndex, ServiceContext
from llama_index.core import BaseQueryEngine
from llama_index.vector_stores import ChromaVectorStore
from llama_index.embeddings import OpenAIEmbedding
from langchain.llms import Ollama
from db import Database

class OllamaLLM:
    def __init__(self, db: Database):
        self.db = db
        self.llm = Ollama(model="llama2")
        self.embedding = OpenAIEmbedding()
    
    def serveUser(self, userid):
        collection = self.db.getCollection(userid)
        vectorStore = ChromaVectorStore(chroma_collection= collection)
        service_context = ServiceContext.from_defaults(llm=self.llm, embed_model=self.embedding)
        index = VectorStoreIndex.from_vector_store(vectorStore, service_context)
        return QueryEngine(index.as_query_engine())
        

class QueryEngine:
    def __init__(self, query_engine: BaseQueryEngine):
        self.query_engine = query_engine
    
    def query(self, query_string):
        return self.query_engine.query(query_string).response
