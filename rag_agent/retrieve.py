from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load maintenance documents
with open("data/manuals.txt", "r") as file:
    documents = file.read().split("\n\n")

# Convert documents into embeddings
doc_embeddings = model.encode(documents)

# Create FAISS index
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add embeddings to index
index.add(np.array(doc_embeddings))

# Example anomaly query
query = "abnormal vibration detected in turbine"

# Convert query into embedding
query_embedding = model.encode([query])

# Search for most relevant document
k = 1
distances, indices = index.search(np.array(query_embedding), k)

# Retrieve best match
best_match = documents[indices[0][0]]

print("QUERY:")
print(query)

print("\nRETRIEVED MAINTENANCE PROCEDURE:")
print(best_match)