import faiss
import numpy as np
import pandas as pd



# Load FAISS index
index = faiss.read_index("data/vectorestore.index")

# Create an array to hold the vectors
vectors = np.zeros((index.ntotal, index.d), dtype=np.float32)

# Retrieve all vectors
for i in range(index.ntotal):
    vectors[i, :] = index.reconstruct(i)  # Reconstruct each vector

print("First 5 Vectors:")
print(vectors[:5])  # Print first 5 embeddings

df = pd.DataFrame(vectors[:20])
df.to_csv("data/vector_data.csv", index=False)

print("Vectors saved to vector_data.csv")