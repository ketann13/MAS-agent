from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from mas_learning_agent.config import (
    LEARNING_EVENTS_COLLECTION,
    LEARNING_RESOURCES_COLLECTION,
    FEEDBACK_LOGS_COLLECTION,
    CONCEPT_STATS_COLLECTION,
    EMBEDDING_MODEL_NAME
)
from sentence_transformers import SentenceTransformer

# Load model just to get vector size
model = SentenceTransformer("all-MiniLM-L6-v2")
VECTOR_SIZE = model.get_sentence_embedding_dimension()

client = QdrantClient(host="localhost", port=6333)


def create_collection(name):
    existing = [c.name for c in client.get_collections().collections]

    if name in existing:
        print(f"✅ Collection already exists: {name}")
        return

    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )
    print(f"🆕 Created collection: {name}")


if __name__ == "__main__":
    create_collection(LEARNING_EVENTS_COLLECTION)
    create_collection(LEARNING_RESOURCES_COLLECTION)
    create_collection(FEEDBACK_LOGS_COLLECTION)
    create_collection(CONCEPT_STATS_COLLECTION)
