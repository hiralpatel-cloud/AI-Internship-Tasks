import os
import face_recognition
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["FaceRecognitionDB"]
collection = db["faces"]

folder = "images"

for filename in os.listdir(folder):

    path = os.path.join(folder, filename)

    image = face_recognition.load_image_file(path)

    encodings = face_recognition.face_encodings(image)

    if len(encodings) > 0:

        embedding = encodings[0]

        name = os.path.splitext(filename)[0]

        data = {
            "name": name,
            "embedding": embedding.tolist()
        }

        collection.insert_one(data)

        print(f"{name} stored successfully.")

    else:
        print(f"No face detected in {filename}")