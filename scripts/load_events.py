import uuid
from embeddings import get_embedding
from qdrant_db.client import get_qdrant_client
from config import LEARNING_EVENTS_COLLECTION

client = get_qdrant_client()

events = [
    {"text": "I used binary search on unsorted array", "concept": "Binary Search", "correct": False},
    {"text": "I forgot base case in recursion", "concept": "Recursion", "correct": False},
    {"text": "I solved DP using recursion and got TLE", "concept": "Dynamic Programming", "correct": False}
]

points = []

for e in events:
    points.append({
        "id": str(uuid.uuid4()),
        "vector": get_embedding(e["text"]),
        "payload": e
    })

client.upsert(collection_name=LEARNING_EVENTS_COLLECTION, points=points)

print("✅ Learning events stored")
