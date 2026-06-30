import streamlit as st
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# Search Libraries
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import chromadb
from pinecone import Pinecone

# Load Environment Variables (.env)
load_dotenv(override=True)

# --- 1. PAGE CONFIGURATION & FIX CSS ---
st.set_page_config(page_title="Vehicle Search Engine", layout="wide")

# Memaksa warna Monochrome (Hitam & Putih) agar tidak bentrok dengan Dark/Light Mode bawaan
st.markdown("""
<style>
    /* Force background and text color on main elements */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, span, label, div { color: #000000 !important; }
    
    /* Input Box Styling */
    .stTextInput > div > div > input {
        border: 1px solid #000000 !important;
        border-radius: 0px !important;
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    
    /* Result Card Styling */
    .result-card {
        background-color: #FAFAFA;
        border: 1px solid #DDDDDD;
        border-left: 5px solid #000000;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .car-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 5px; }
    .car-price { font-size: 1.1rem; font-weight: 600; color: #444444 !important; margin-bottom: 10px; }
    .car-specs { background-color: #E0E0E0; padding: 4px 10px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin-bottom: 10px; }
    .car-desc { font-size: 0.95rem; color: #333333 !important; line-height: 1.5; }
    .car-metric { font-size: 0.8rem; color: #777777 !important; margin-top: 15px; font-style: italic; border-top: 1px dashed #CCC; padding-top: 5px;}
    
    /* Hide default streamlit footer & header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# --- 2. CACHED DATA & MODELS ---
@st.cache_resource
def load_system():
    # 1. Load Data
    df = pd.read_csv('data_mobil.csv')
    df['price_formatted'] = df['price_idr'].apply(lambda x: f"Rp {x:,.0f}".replace(',', '.'))
    df['searchable_text'] = (df['brand'].fillna('') + ' ' + 
                             df['model'].fillna('') + ' ' + 
                             df['specs'].fillna('') + ' ' + 
                             df['description'].fillna(''))
    corpus = df['searchable_text'].tolist()

    # 2. Setup Keyword Search (BM25 & TF-IDF)
    tokenized_corpus = [doc.lower().split() for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)

    tfidf_vectorizer = TfidfVectorizer(stop_words=None, ngram_range=(1, 2))
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

    # 3. Setup Embedding Model
    embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # 4. Setup ChromaDB (Local)
    chroma_client = chromadb.PersistentClient(path="./chroma_mobil")
    try:
        collection = chroma_client.get_collection(name="mobil_collection")
    except:
        collection = chroma_client.create_collection(name="mobil_collection", metadata={"hnsw:space": "cosine"})
        embeddings = embedding_model.encode(corpus)
        collection.add(
            embeddings=embeddings.tolist(),
            documents=corpus,
            metadatas=[{
                'brand_model': f"{row['brand']} {row['model']}",
                'year': str(row['year']),
                'price': row['price_formatted'],
                'specs': row['specs'],
                'description': row['description']
            } for _, row in df.iterrows()],
            ids=[str(row['id']) for _, row in df.iterrows()]
        )

    # 5. Setup Pinecone (Cloud)
    pinecone_index = None
    api_key = os.getenv('PINECONE_API_KEY')
    if api_key:
        try:
            pc = Pinecone(api_key=api_key)
            if 'mobil-search' in pc.list_indexes().names():
                pinecone_index = pc.Index('mobil-search')
        except:
            pass

    return df, corpus, bm25, tfidf_vectorizer, tfidf_matrix, embedding_model, collection, pinecone_index

df, corpus, bm25, tfidf_vectorizer, tfidf_matrix, embedding_model, collection, pinecone_index = load_system()


# --- 3. SEARCH LOGIC ---
def search_vehicles(query, method, top_k=5):
    results_list = []
    
    if method == "BM25 (Keyword Search)":
        tokenized_query = query.lower().split()
        scores = bm25.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:top_k]
        for idx in top_indices:
            if scores[idx] > 0:
                row = df.iloc[idx]
                results_list.append({
                    'title': f"{row['brand']} {row['model']} ({row['year']})",
                    'price': row['price_formatted'],
                    'specs': row['specs'],
                    'desc': row['description'],
                    'metric': f"BM25 Score: {scores[idx]:.4f}"
                })

    elif method == "TF-IDF (Keyword Search)":
        query_vec = tfidf_vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        top_indices = np.argsort(similarities)[::-1][:top_k]
        for idx in top_indices:
            if similarities[idx] > 0:
                row = df.iloc[idx]
                results_list.append({
                    'title': f"{row['brand']} {row['model']} ({row['year']})",
                    'price': row['price_formatted'],
                    'specs': row['specs'],
                    'desc': row['description'],
                    'metric': f"Cosine Similarity: {similarities[idx]:.4f}"
                })

    elif method == "ChromaDB (Semantic Search)":
        query_embedding = embedding_model.encode([query])
        results = collection.query(query_embeddings=query_embedding.tolist(), n_results=top_k)
        for i in range(len(results['ids'][0])):
            meta = results['metadatas'][0][i]
            results_list.append({
                'title': f"{meta['brand_model']} ({meta['year']})",
                'price': meta['price'],
                'specs': meta['specs'],
                'desc': meta.get('description', ''),
                'metric': f"ChromaDB Distance: {results['distances'][0][i]:.4f}"
            })
            
    elif method == "Pinecone (Semantic Search)":
        if not pinecone_index:
            st.error("Pinecone API Key tidak ditemukan atau index belum dibuat di Cloud.")
            return []
        
        query_embedding = embedding_model.encode([query])
        results = pinecone_index.query(vector=query_embedding.tolist()[0], top_k=top_k, include_metadata=True)
        
        for match in results['matches']:
            meta = match['metadata']
            results_list.append({
                'title': f"{meta['brand_model']} ({meta['year']})",
                'price': meta['price'],
                'specs': meta['specs'],
                'desc': meta.get('description', ''),
                'metric': f"Pinecone Similarity Score: {match['score']:.4f}"
            })
            
    return results_list


# --- 4. USER INTERFACE (UI) ---
st.title("VEHICLE SEARCH ENGINE")
st.write("Intelligent search system combining Keyword & Semantic Analysis.")
st.markdown("<hr style='border: 1px solid #000; margin-top: 0px;'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### CONFIGURATION")
    search_method = st.radio(
        "Select Search Algorithm:",
        ("ChromaDB (Semantic Search)", "Pinecone (Semantic Search)", "BM25 (Keyword Search)", "TF-IDF (Keyword Search)")
    )
    
    st.markdown("<br><b>TEST QUERIES</b>", unsafe_allow_html=True)
    st.markdown("- Mobil yang cocok untuk keluarga")
    st.markdown("- Mobil Listrik")
    st.markdown("- Mobil Autopilot")
    st.markdown("- Mobil hemat bahan bakar")
    st.markdown("- Mobil murah dibawah 250 juta")

with col2:
    query = st.text_input("", placeholder="Enter keywords or semantic context here...")
    
    if query:
        st.markdown(f"**Results for:** '{query}'")
        
        # Eksekusi pencarian
        results = search_vehicles(query, method=search_method, top_k=3)
        
        if not results:
            st.warning("No matches found. Try another query.")
        else:
            for res in results:
                st.markdown(f"""
                <div class="result-card">
                    <div class="car-title">{res['title']}</div>
                    <div class="car-price">{res['price']}</div>
                    <div class="car-specs">{res['specs']}</div>
                    <div class="car-desc">{res['desc']}</div>
                    <div class="car-metric">Search Engine Metric | {res['metric']}</div>
                </div>
                """, unsafe_allow_html=True)