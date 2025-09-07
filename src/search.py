import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os

# Paths
CSV_PATH = '../data/workflows.csv'
EMBEDDING_PATH = '../embeddings/workflow_embeddings.npy'
INDEX_PATH = '../embeddings/faiss_index.index'

class CSVSearchEngine:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        """Load all necessary data and models"""
        print("Loading search engine...")
        
        # Check if files exist
        if not os.path.exists(CSV_PATH):
            print(f"Error: CSV file not found at {CSV_PATH}")
            return False
            
        if not os.path.exists(EMBEDDING_PATH):
            print(f"Error: Embeddings not found at {EMBEDDING_PATH}")
            print("Please run build_index.py first!")
            return False
            
        if not os.path.exists(INDEX_PATH):
            print(f"Error: FAISS index not found at {INDEX_PATH}")
            print("Please run build_index.py first!")
            return False
        
        # Load CSV
        self.df = pd.read_csv(CSV_PATH)
        
        # Load embeddings
        self.embeddings = np.load(EMBEDDING_PATH)
        
        # Load FAISS index
        self.index = faiss.read_index(INDEX_PATH)
        
        # Load model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        print("Search engine loaded successfully!")
        return True

    def search(self, query, k=5):
        """Search for similar workflows"""
        if not hasattr(self, 'model'):
            print("Search engine not properly loaded!")
            return
            
        # Generate query embedding
        query_emb = self.model.encode([query])
        query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)
        
        # Search
        D, I = self.index.search(query_emb, k)
        
        print(f"\nTop {k} results for: '{query}'")
        print("-" * 50)
        
        for i, idx in enumerate(I[0]):
            score = D[0][i]
            workflow_name = self.df.iloc[idx]['workflow_name']
            workflow_id = self.df.iloc[idx]['workflow_id']
            print(f"{i+1}. {workflow_name}")
            print(f"   Workflow ID: {workflow_id}")
            print(f"   Similarity Score: {score:.4f}")
            print()

def main():
    # Initialize search engine
    search_engine = CSVSearchEngine()
    
    if not hasattr(search_engine, 'model'):
        return
    
    print("\n" + "="*60)
    print("CSV SEARCH ENGINE - CLI Interface")
    print("="*60)
    print("Type your search queries below. Type 'exit' to quit.")
    print("Example queries: 'email automation', 'data scraping', 'notifications'")
    print("-"*60)
    
    while True:
        try:
            query = input("\nEnter search query: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
                
            if not query:
                print("Please enter a search query.")
                continue
                
            search_engine.search(query)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
