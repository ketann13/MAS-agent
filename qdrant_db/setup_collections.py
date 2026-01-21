from qdrant_client.models import VectorParams, Distance
from .client import get_qdrant_client
from ..config import (
    LEARNING_EVENTS_COLLECTION,
    LEARNING_RESOURCES_COLLECTION,
)

VECTOR_SIZE = 384


def setup():
    client = get_qdrant_client()

    client.recreate_collection(
        collection_name=LEARNING_EVENTS_COLLECTION,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )

    client.recreate_collection(
        collection_name=LEARNING_RESOURCES_COLLECTION,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    client.recreate_collection(
    collection_name="concept_stats",
    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
)

    client.recreate_collection(
    collection_name="feedback_logs",
    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
)


    print("✅ Qdrant collections created successfully")


if __name__ == "__main__":
    setup()
