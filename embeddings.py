import streamlit as st
from sentence_transformers import SentenceTransformer
from mas_learning_agent.config import EMBEDDING_MODEL_NAME

@st.cache_resource
def load_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)

def get_embedding(text: str):
    model = load_model()
    return model.encode(text).tolist()

