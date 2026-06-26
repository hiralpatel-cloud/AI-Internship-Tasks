from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["FaceRecognitionDB"]

collection = db["faces"]

print("Database and collection created successfully!")