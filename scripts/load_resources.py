import json
from embeddings import get_embedding
from qdrant_db.client import get_qdrant_client
from config import LEARNING_RESOURCES_COLLECTION

client = get_qdrant_client()

with open("data/resources.json", "r") as f:
    resources = json.load(f)

points = []

for r in resources:
    points.append({
        "id": r["id"],
        "vector": get_embedding(r["text"]),
        "payload": r
    })

client.upsert(collection_name=LEARNING_RESOURCES_COLLECTION, points=points)

print("✅ Learning resources loaded into Qdrant")
