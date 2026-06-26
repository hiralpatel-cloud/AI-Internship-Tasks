from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["FaceRecognitionDB"]
collection = db["faces"]

for person in collection.find():
    print("Name:", person["name"])
    print("Embedding Length:", len(person["embedding"]))
    print("-" * 30)