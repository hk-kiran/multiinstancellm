import os
import db.db as db
from llms.llm import LLM
import time

user1 = "user1"
user2 = "user2"

def initDatabase():
    database = db.Database("localhost", 8000)
    database.checkHeartBeat()
    return database

database = initDatabase()
database.createCollection(user1, {"type": "test"})
database.createCollection(user2, {"type": "test"})
database.addPDF(user1, os.path.abspath("./data/user1/sampletext.pdf"))
database.addPDF(user2, os.path.abspath("./data/user2/sampletext.pdf"))

llm = LLM(database).init()
user1Instance = llm.serveUser(user1)
user2Instance = llm.serveUser(user2)

resp1 = user1Instance.query("Where did the old man sit? And what did he feed?")
resp2 = user2Instance.query("Where did the old man sit? And what did he feed?")

print(resp1)
print(resp2)

# while True:
#     user_input = input("Enter your query: ")
#     if user_input == "exit":
#         break
#     resp = user1Instance.query(user_input)
#     print(resp)
