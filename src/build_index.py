import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os

# Paths
CSV_PATH = '../data/workflows.csv'
EMBEDDING_PATH = '../embeddings/workflow_embeddings.npy'
INDEX_PATH = '../embeddings/faiss_index.index'

def build_index():
    # Load CSV
    print("Loading CSV data...")
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} workflows")

    # Load model
    print("Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate embeddings
    print("Generating embeddings...")
    # Use workflow_name as the searchable text
    searchable_text = df['workflow_name'].fillna('').astype(str).tolist()
    embeddings = model.encode(searchable_text, convert_to_numpy=True)
    print(f"Generated embeddings with shape: {embeddings.shape}")

    # Normalize embeddings for cosine similarity
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # Save embeddings
    os.makedirs('../embeddings', exist_ok=True)
    np.save(EMBEDDING_PATH, embeddings)
    print(f"Embeddings saved to {EMBEDDING_PATH}")

    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # cosine similarity
    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(index, INDEX_PATH)
    print(f"FAISS index saved to {INDEX_PATH}")
    print("Index built and saved successfully!")

if __name__ == "__main__":
    build_index()
