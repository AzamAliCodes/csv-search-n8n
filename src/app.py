6

import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os

# Paths
CSV_PATH = '../data/workflows.csv'
EMBEDDING_PATH = '../embeddings/workflow_embeddings.npy'
INDEX_PATH = '../embeddings/faiss_index.index'

@st.cache_resource
def load_search_engine():
    """Load all necessary data and models (cached for performance)"""
    try:
        # Check if files exist
        if not os.path.exists(CSV_PATH):
            st.error(f"CSV file not found at {CSV_PATH}")
            return None, None, None, None
            
        if not os.path.exists(EMBEDDING_PATH):
            st.error(f"Embeddings not found at {EMBEDDING_PATH}")
            st.error("Please run build_index.py first!")
            return None, None, None, None
            
        if not os.path.exists(INDEX_PATH):
            st.error(f"FAISS index not found at {INDEX_PATH}")
            st.error("Please run build_index.py first!")
            return None, None, None, None
        
        # Load data
        df = pd.read_csv(CSV_PATH)
        embeddings = np.load(EMBEDDING_PATH)
        index = faiss.read_index(INDEX_PATH)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        return df, embeddings, index, model
    
    except Exception as e:
        st.error(f"Error loading search engine: {e}")
        return None, None, None, None

def search_workflows(query, df, index, model, k=5):
    """Search for similar workflows"""
    # Generate query embedding
    query_emb = model.encode([query])
    query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)
    
    # Search
    D, I = index.search(query_emb, k)
    
    results = []
    for i, idx in enumerate(I[0]):
        score = D[0][i]
        workflow_name = df.iloc[idx]['workflow_name']
        workflow_id = df.iloc[idx]['workflow_id']
        workflow_json = df.iloc[idx]['workflow_json']
        results.append({
            'rank': i + 1,
            'workflow_name': workflow_name,
            'workflow_id': workflow_id,
            'workflow_json': workflow_json,
            'score': score
        })
    
    return results

# Streamlit App
def main():
    st.set_page_config(
        page_title="CSV Search Engine",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 CSV Search Engine")
    st.markdown("Search through your workflow data using semantic similarity")
    
    # Load search engine
    df, embeddings, index, model = load_search_engine()
    
    if df is None:
        st.stop()
    
    # Sidebar with info
    with st.sidebar:
        st.header("📊 Dataset Info")
        st.write(f"Total workflows: {len(df)}")
        st.write(f"Embedding dimension: {embeddings.shape[1]}")
        
        st.header("💡 Example Queries")
        example_queries = [
            "email automation",
            "data scraping",
            "notifications",
            "file backup",
            "social media",
            "payment processing"
        ]
        
        for query in example_queries:
            if st.button(f"'{query}'", key=f"example_{query}"):
                st.session_state.search_query = query
    
    # Main search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Enter your search query:",
            value=st.session_state.get('search_query', ''),
            placeholder="e.g., email automation, data scraping, notifications..."
        )
    
    with col2:
        num_results = st.selectbox("Results to show:", [5, 10, 15], index=0)
    
    if query:
        with st.spinner('Searching...'):
            results = search_workflows(query, df, index, model, k=num_results)
        
        st.subheader(f"🎯 Top {len(results)} Results for: '{query}'")
        
        # Display results
        for result in results:
            with st.expander(f"#{result['rank']} - {result['workflow_name']} (Score: {result['score']:.4f})", expanded=True):
                st.write("**Workflow ID:**")
                st.write(result['workflow_id'])
                
                st.write("**Workflow JSON:**")
                st.code(result['workflow_json'], language='json')
                
                # Progress bar for similarity score
                st.write("**Similarity Score:**")
                score_percentage = max(0, min(100, result['score'] * 100))
                st.progress(float(score_percentage / 100))
                st.caption(f"Score: {result['score']:.4f}")
        
        # Download results
        if st.button("📥 Download Results as CSV"):
            results_df = pd.DataFrame(results)
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"search_results_{query.replace(' ', '_')}.csv",
                mime="text/csv"
            )
    
    else:
        st.info("👆 Enter a search query above to find relevant workflows")
        
        # Show sample data
        st.subheader("📋 Sample Data")
        st.dataframe(df.head(10), width='stretch')

if __name__ == "__main__":
    main()


