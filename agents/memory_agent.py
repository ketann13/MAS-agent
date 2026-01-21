from embeddings import get_embedding
from qdrant_db.client import get_qdrant_client
from config import LEARNING_EVENTS_COLLECTION, TOP_K_MEMORY
import uuid
import time

client = get_qdrant_client()


def store_event(text, concept, correct):
    point = {
        "id": str(uuid.uuid4()),
        "vector": get_embedding(text),
        "payload": {
            "text": text,
            "concept": concept,
            "correct": correct,
            "timestamp": time.time()
        }
    }
    client.upsert(collection_name=LEARNING_EVENTS_COLLECTION, points=[point])


def get_similar_events(query_text):
    results = client.query_points(
        collection_name=LEARNING_EVENTS_COLLECTION,
        query=get_embedding(query_text),
        limit=TOP_K_MEMORY,
        with_payload=True
    )

    return [p.payload for p in results.points]

def store_concept_stat(concept):
    point = {
        "id": str(uuid.uuid4()),
        "vector": get_embedding(concept),
        "payload": {"concept": concept}
    }
    client.upsert(collection_name="concept_stats", points=[point])
