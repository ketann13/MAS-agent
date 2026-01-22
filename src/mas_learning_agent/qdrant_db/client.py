from qdrant_client import QdrantClient

_client = None

def get_qdrant_client():
    global _client
    if _client is not None:
        return _client

    try:
        _client = QdrantClient(host="localhost", port=6333)
        print("✅ Connected to local Qdrant")
        return _client
    except Exception as e:
        print("❌ Qdrant connection error:", e)
        return None
    return _client  