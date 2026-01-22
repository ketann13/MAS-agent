import json
import sys
import os

# ---------- PATH SETUP ----------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

# ---------- IMPORTS ----------
from mas_learning_agent.embeddings import get_embedding
from mas_learning_agent.qdrant_db.client import get_qdrant_client
from mas_learning_agent.config import LEARNING_RESOURCES_COLLECTION

# ---------- QDRANT ----------
client = get_qdrant_client()
if client is None:
    raise RuntimeError("❌ Qdrant client is not available. Check Qdrant connection settings.")

print("✅ Connected to Qdrant")

# ---------- LOAD DATA ----------
data_path = os.path.join(PROJECT_ROOT, "data", "resources.json")

with open(data_path, "r", encoding="utf-8") as f:
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
