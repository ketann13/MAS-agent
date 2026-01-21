import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from ..config import LEARNING_EVENTS_COLLECTION, LEARNING_RESOURCES_COLLECTION

VECTOR_SIZE = 384


def get_qdrant_client():
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not url or not api_key:
        raise RuntimeError("QDRANT_URL or QDRANT_API_KEY missing in env")

    client = QdrantClient(url=url, api_key=api_key)

    try:
        existing = [c.name for c in client.get_collections().collections]
    except Exception as e:
        print("❌ Qdrant connection failed:", e)
        raise RuntimeError("Cannot connect to Qdrant Cloud")

    def create_if_missing(name):
        if name not in existing:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )
            print("✅ Created collection:", name)

    create_if_missing(LEARNING_EVENTS_COLLECTION)
    create_if_missing(LEARNING_RESOURCES_COLLECTION)
    create_if_missing("feedback_logs")

    return client
