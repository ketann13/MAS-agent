from qdrant_client import QdrantClient
from config import QDRANT_URL

_client = None


def get_qdrant_client():
    global _client
    if _client is None:
        print("🔌 Connecting to Qdrant...")
        _client = QdrantClient(url=QDRANT_URL)
    return _client
