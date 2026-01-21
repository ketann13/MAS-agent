import os
from qdrant_client import QdrantClient

_client = None

def get_qdrant_client():
    global _client

    if _client is not None:
        return _client

    try:
        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")

        if not url or not api_key:
            raise ValueError("Missing Qdrant credentials")

        _client = QdrantClient(url=url, api_key=api_key)
        return _client

    except Exception as e:
        print("❌ Qdrant connection error:", e)
        return None   # ❗ DO NOT CRASH APP
