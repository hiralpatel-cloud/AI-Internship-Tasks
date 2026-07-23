import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read knowledge base
with open("knowledge.txt", "r", encoding="utf-8") as file:
    documents = [line.strip() for line in file if line.strip()]

# Create embeddings
embeddings = model.encode(documents)
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print("\nMini RAG Chatbot")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("Bot: Goodbye!")
        break

    # Convert question into embedding
    query_embedding = model.encode([question])
    query_embedding = np.array(query_embedding).astype("float32")

    # Search similar documents
    k = 2
    distances, indices = index.search(query_embedding, k)

    # Build context
    context = "\n".join([documents[i] for i in indices[0]])

    prompt = f"""
Use only the following context to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    print("\nBot:", response.text)