from ..embeddings import get_embedding
from ..qdrant_db.client import get_qdrant_client
from ..config import LEARNING_RESOURCES_COLLECTION, TOP_K_RESOURCES
import uuid

client = get_qdrant_client()


def get_resources_for_concept(concept_text):
    results = client.query_points(
        collection_name=LEARNING_RESOURCES_COLLECTION,
        query=get_embedding(concept_text),
        limit=TOP_K_RESOURCES,
        with_payload=True
    )

    # remove duplicate texts
    seen = set()
    unique = []
    for p in results.points:
        if p.payload["text"] not in seen:
            unique.append(p.payload)
            seen.add(p.payload["text"])

    return unique


def store_new_resource(text, concept):
    point = {
        "id": str(uuid.uuid4()),
        "vector": get_embedding(text),
        "payload": {
            "text": text,
            "concept": concept,
            "source": "user_feedback"
        }
    }

    client.upsert(
        collection_name=LEARNING_RESOURCES_COLLECTION,
        points=[point]
    )


def store_feedback(text, concept, helpful):
    point = {
        "id": str(uuid.uuid4()),
        "vector": get_embedding(text),
        "payload": {
            "concept": concept,
            "helpful": helpful
        }
    }

    client.upsert(collection_name="feedback_logs", points=[point])
