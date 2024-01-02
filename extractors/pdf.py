from llama_index import SimpleDirectoryReader

documents = SimpleDirectoryReader("../data/user1/").load_data()