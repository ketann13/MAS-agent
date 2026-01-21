import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from config import (
    LEARNING_EVENTS_COLLECTION,
    LEARNING_RESOURCES_COLLECTION,
)

VECTOR_SIZE = 384


def get_qdrant_client():
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not url or not api_key:
        raise ValueError("❌ QDRANT_URL or QDRANT_API_KEY not set in environment")

    client = QdrantClient(url=url, api_key=api_key)

    # -------- AUTO CREATE COLLECTIONS --------
    existing = [c.name for c in client.get_collections().collections]

    if LEARNING_EVENTS_COLLECTION not in existing:
        client.create_collection(
            collection_name=LEARNING_EVENTS_COLLECTION,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print("✅ Created:", LEARNING_EVENTS_COLLECTION)

    if LEARNING_RESOURCES_COLLECTION not in existing:
        client.create_collection(
            collection_name=LEARNING_RESOURCES_COLLECTION,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print("✅ Created:", LEARNING_RESOURCES_COLLECTION)

    if "feedback_logs" not in existing:
        client.create_collection(
            collection_name="feedback_logs",
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print("✅ Created: feedback_logs")

    return client
