import os
import chromadb
import time
import db_utils
from llama_index import SimpleDirectoryReader
import json

class Database:

    def __init__(self, ip, port):
        self.db = db_utils.connect_to_database(ip, port)
        self.ef = db_utils.getOpenAIEmbeddingFunc()
        self.n_nearest = 5
    
    def checkHeartBeat(self):
        self.db.heartbeat()

    def createCollection(self, name, meta):

        return self.db.create_collection(
            name=name,
            embedding_function= self.ef,
            get_or_create= True,
            metadata= meta
        )
    
    def getCollection(self, name):

        return self.db.get_collection(name=name, embedding_function= self.ef)

    def listCollections(self):

        return self.db.list_collections()
    
    def addPDF(self, collectionName, documentPath):
        collection = self.getCollection(collectionName)
        pdf = SimpleDirectoryReader(input_files=[documentPath]).load_data()
        # pdf[0].dict() = 
        #
        #         {
        #     "id_": "6cffd5d6-93e3-46ab-8a08-d86d1f8b4773",
        #     "embedding": null,
        #     "metadata": {
        #         "page_label": "1",
        #         "file_name": "sampletext.pdf",
        #         "file_path": "/Users/kiranhk/Projects/multiinstancellm/data/user1/sampletext.pdf",
        #         "file_type": "application/pdf",
        #         "file_size": 2732,
        #         "creation_date": "2023-12-23",
        #         "last_modified_date": "2023-12-23",
        #         "last_accessed_date": "2023-12-23"
        #     },
        #     "excluded_embed_metadata_keys": [
        #         "file_name",
        #         "file_type",
        #         "file_size",
        #         "creation_date",
        #         "last_modified_date",
        #         "last_accessed_date"
        #     ],
        #     "excluded_llm_metadata_keys": [
        #         "file_name",
        #         "file_type",
        #         "file_size",
        #         "creation_date",
        #         "last_modified_date",
        #         "last_accessed_date"
        #     ],
        #     "relationships": {},
        #     "hash": "ee8556c2088a193a6bed840d73fca31f95ad1aa66d908e83046ad8b8e8c3d1d3",
        #     "text": " \nThe Wonders of AI: Unveiling a World of Possibilities",
        #     "start_char_idx": null,
        #     "end_char_idx": null,
        #     "text_template": "{metadata_str}\n\n{content}",
        #     "metadata_template": "{key}: {value}",
        #     "metadata_seperator": "\n",
        #     "class_name": "Document"
        # }

        pdf_dict = pdf[0].dict()
        collection.upsert(ids= [pdf_dict["id_"]], metadatas=pdf_dict["metadata"], documents=[pdf_dict["text"]])
        # collection.update()

    def printCollection(self, collection):

        return self.getCollection(collection).get(include=["documents", "embeddings"])
    
    def query(self, collection: str, query: str):

        return self.getCollection(collection).query(include=["documents", "embeddings"],query_texts=[query], n_results= self.n_nearest)

        
if __name__ == '__main__':

    db = Database("localhost", 8000)
    db.checkHeartBeat()
    # db.createCollection("test", {"name": "test"})
    # db.addPDF("test", os.path.abspath("./data/user1/sampletext.pdf"))
    result = db.printCollection("user1")
    # query_result = db.query("test", "what are self-driving cars")
    print(result)
    print("------------")
    # print(query_result)
