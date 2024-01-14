from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.embeddings import OpenAIEmbedding
from llama_index.llms import LlamaCPP
from langchain.llms import Ollama
from langchain.embeddings import HuggingFaceEmbeddings
from src.db.db import Database
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt
from src.llms.llm_utils import BaseLLM, QueryEngine
from jproperties import Properties

class LLM:
    def __init__(self, db: Database):
        self.db = db
        self.properties = Properties()
        with open('model.properties', 'rb') as file:
            self.properties.load(file)
            self.properties = self.properties.properties
            
    def init(self) -> BaseLLM:
        match self.properties["model_name"]:
            case 'ollama':
                return OllamaLLM(self.db)
            case 'llama-cpp':
                return LlamaCpp(self.db, self.properties)
            case _ :
                return OllamaLLM(self.db)
            
class LlamaCpp(BaseLLM):
    def __init__(self, db: Database, properties: dict) -> None:
        self.db = db
        self.llm = LlamaCPP(
            model_path=properties['llamaCppPath'],
            temperature=0.1,
            context_window=3900,
            model_kwargs={"n_gpu_layers": int(properties['gpu'])},
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=properties['llamaCppVerbose'] == "True",
        )

        if properties["useOpenAI"] ["useOpenAI"] == "True":
            self.embedding = OpenAIEmbedding()
        else:
            self.embedding = HuggingFaceEmbeddings(
                model_name=properties["huggingFaceEmbeddingModel"],
            )

    def serveUser(self, userid: str):
        collection = self.db.getCollection(userid)
        vectorStore = ChromaVectorStore(chroma_collection= collection)
        service_context = ServiceContext.from_defaults(llm=self.llm, embed_model=self.embedding)
        index = VectorStoreIndex.from_vector_store(vectorStore, service_context)
        return QueryEngine(index.as_query_engine())


class OllamaLLM(BaseLLM):
    def __init__(self, db: Database):
        self.db = db
        self.llm = Ollama(model="llama2")
        self.embedding = OpenAIEmbedding()
    
    def serveUser(self, userid: str):
        collection = self.db.getCollection(userid)
        vectorStore = ChromaVectorStore(chroma_collection= collection)
        service_context = ServiceContext.from_defaults(llm=self.llm, embed_model=self.embedding)
        index = VectorStoreIndex.from_vector_store(vectorStore, service_context)
        return QueryEngine(index.as_query_engine())
        
