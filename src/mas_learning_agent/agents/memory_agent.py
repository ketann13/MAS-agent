from mas_learning_agent.embeddings import get_embedding
from mas_learning_agent.qdrant_db.client import get_qdrant_client
from mas_learning_agent.config import LEARNING_EVENTS_COLLECTION, TOP_K_MEMORY
from qdrant_client.http.models import PointStruct
import uuid
import time


def store_event(text, concept, correct):
    client = get_qdrant_client()
    if client is None:
        print("⚠ Skipping memory store (no Qdrant)")
        return

    concept = (concept or "").strip().lower()

    try:
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=get_embedding(text),
            payload={
                "text": text,
                "concept": concept,
                "correct": correct,
                "timestamp": time.time(),
            },
        )
        client.upsert(collection_name=LEARNING_EVENTS_COLLECTION, points=[point])

    except Exception as e:
        print("❌ Qdrant upsert failed:", e)

def get_similar_events(query_text):
    client = get_qdrant_client()
    if client is None:
        return []
    
    results = client.query_points(
        collection_name=LEARNING_EVENTS_COLLECTION,
        query=get_embedding(query_text),
        limit=TOP_K_MEMORY,
        with_payload=True
    )

    return [p.payload for p in results.points]

def store_concept_stat(concept):
    client = get_qdrant_client()
    if client is None:
        return

    concept = (concept or "").strip().lower()
    
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=get_embedding(concept),
        payload={"concept": concept},
    )
    client.upsert(collection_name="concept_stats", points=[point])
