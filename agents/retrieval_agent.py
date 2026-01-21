from mas_learning_agent.embeddings import get_embedding
from mas_learning_agent.qdrant_db.client import get_qdrant_client
from mas_learning_agent.config import LEARNING_RESOURCES_COLLECTION, TOP_K_RESOURCES
import uuid


def get_resources_for_concept(concept_text):
    client = get_qdrant_client()
    if client is None:
        return []
    
    try:
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
    except Exception:
        return []


def store_new_resource(text, concept):
    client = get_qdrant_client()
    if client is None:
        return
    
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
    client = get_qdrant_client()
    if client is None:
        return
    
    point = {
        "id": str(uuid.uuid4()),
        "vector": get_embedding(text),
        "payload": {
            "concept": concept,
            "helpful": helpful
        }
    }

    client.upsert(collection_name="feedback_logs", points=[point])
