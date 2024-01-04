from abc import ABC, abstractmethod
from llama_index.core import BaseQueryEngine

class BaseLLM(ABC):
    @abstractmethod
    def serveUser(self, userid: str):
        raise NotImplementedError

class QueryEngine:
    def __init__(self, query_engine: BaseQueryEngine):
        self.query_engine = query_engine
    
    def query(self, query_string):
        return self.query_engine.query(query_string).response