from agents.memory_agent import store_event, get_similar_events
from agents.pattern_agent import detect_weak_concepts
from agents.retrieval_agent import get_resources_for_concept
from agents.recommendation_agent import generate_recommendation


def handle_student_input(text, concept, correct=False):
    concept = concept.strip().lower()
    store_event(text, concept, correct)

    similar_events = get_similar_events(text)

    weak_concepts = detect_weak_concepts(similar_events)

    resources = []
    for c in weak_concepts:
        resources.extend(get_resources_for_concept(c))

    recommendation = generate_recommendation(
        weak_concepts,
        resources,
        similar_events
    )

    recommendation["original_input"] = text
    recommendation["concept"] = concept
    return recommendation
    
