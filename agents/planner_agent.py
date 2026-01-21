from mas_learning_agent.agents.memory_agent import store_event, get_similar_events
from mas_learning_agent.agents.pattern_agent import detect_weak_concepts
from mas_learning_agent.agents.retrieval_agent import get_resources_for_concept
from mas_learning_agent.agents.recommendation_agent import generate_recommendation
from mas_learning_agent.agents.llm_agent import generate_explanation


def normalize_concept(concept):
    concept = concept.lower().strip()

    mapping = {
        "dsa": "data structures and algorithms",
        "data structure and algo": "data structures and algorithms",
        "data sturecture and algo": "data structures and algorithms",
        "computer networks": "computer networks",
        "comp networks": "computer networks",
    }

    return mapping.get(concept, concept)



def handle_student_input(text, concept, correct=False):

    concept = concept.strip().lower()

    # ---- MEMORY AGENT ----
    store_event(text, concept, correct)
    similar_events = get_similar_events(text)

    # ---- PATTERN AGENT ----
    weak_concepts = detect_weak_concepts(similar_events, concept)

    # ---- TASK ROUTING (MAS ORCHESTRATOR) ----
    if len(similar_events) >= 3:
        task_type = "remediation"
    elif len(similar_events) == 0:
        task_type = "onboarding"
    else:
        task_type = "practice"

    # ---- RETRIEVAL AGENT (OPTIONAL SUPPORT) ----
    # Always prioritize current concept
    resources = get_resources_for_concept(concept)

    # Add weak concept resources if needed
    for c in weak_concepts:
       if c != concept:
        resources.extend(get_resources_for_concept(c))


    # ---- RECOMMENDATION AGENT ----
    advice = generate_recommendation(
        weak_concepts,
        resources,
        similar_events
    )

    # ---- LLM TUTOR AGENT ----
    ai_text = generate_explanation(
    text,
    weak_concepts,
    resources,
    task_type
)


    return {
        "similar_mistakes": similar_events,
        "weak_concepts": weak_concepts,
        "task_type": task_type,
        "resources": resources,
        "advice": advice,
        "ai_explanation": ai_text,
        "agents_used": [
            "Memory Agent",
            "Pattern Agent",
            "Retrieval Agent",
            "Recommendation Agent",
            "LLM Tutor Agent"
        ]
    }
