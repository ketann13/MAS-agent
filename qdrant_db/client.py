import os
from qdrant_client import QdrantClient
from qdrant_client.http import models

_client = None

COLLECTION_NAME = "learning_events"
VECTOR_SIZE = 384   # must match sentence-transformer

def get_qdrant_client():
    global _client

    if _client is not None:
        return _client

    try:
        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")

        if not url or not api_key:
            raise ValueError("Missing Qdrant credentials")

        client = QdrantClient(url=url, api_key=api_key)

        # ✅ ensure collection exists
        existing = [c.name for c in client.get_collections().collections]

        if COLLECTION_NAME not in existing:
            print("⚠ Creating Qdrant collection:", COLLECTION_NAME)
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=VECTOR_SIZE,
                    distance=models.Distance.COSINE,
                ),
            )

        _client = client
        return _client

    except Exception as e:
        print("❌ Qdrant connection error:", e)
        return None
