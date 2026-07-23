import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read knowledge base
with open("knowledge.txt", "r", encoding="utf-8") as file:
    documents = file.readlines()

# Remove empty lines
documents = [doc.strip() for doc in documents if doc.strip()]

print("\nKnowledge Base:")
for i, doc in enumerate(documents):
    print(f"{i+1}. {doc}")

# Create embeddings
embeddings = model.encode(documents)

# Convert to NumPy float32
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add embeddings to FAISS
index.add(embeddings)

print(f"\nTotal documents stored: {index.ntotal}")

# Ask user a question
query = input("\nAsk a question: ")

# Convert question into embedding
query_embedding = model.encode([query])
query_embedding = np.array(query_embedding).astype("float32")

# Search
k = 3
distances, indices = index.search(query_embedding, k)

print("\nTop Matches:\n")

for i in range(k):
    print(f"{i+1}. {documents[indices[0][i]]}")