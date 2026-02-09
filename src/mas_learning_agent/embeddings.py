from functools import lru_cache

from sentence_transformers import SentenceTransformer
from mas_learning_agent.config import EMBEDDING_MODEL_NAME


@lru_cache(maxsize=1)
def load_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def get_embedding(text: str):
    model = load_model()
    return model.encode(text).tolist()

