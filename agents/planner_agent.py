from agents.memory_agent import store_event, get_similar_events
from agents.pattern_agent import detect_weak_concepts
from agents.retrieval_agent import get_resources_for_concept
from agents.recommendation_agent import generate_recommendation



def handle_student_input(text, concept, correct=False):
    concept = concept.strip().lower()

    store_event(text, concept, correct)

    similar_events = get_similar_events(text)

    weak_concepts = detect_weak_concepts(similar_events)

    # -------- TASK ROUTING (MAS ORCHESTRATION) --------
    task_type = "practice"

    if len(similar_events) >= 2:
        task_type = "remediation"
    elif len(similar_events) == 0:
        task_type = "onboarding"

    # -------- RESOURCE RETRIEVAL --------
    resources = []
    for c in weak_concepts:
        resources.extend(get_resources_for_concept(c))

    # -------- RECOMMENDATION --------
    recommendation = generate_recommendation(
        weak_concepts,
        resources,
        similar_events
    )

    # -------- TASK-AWARE ADVICE --------
    advice = []

    if task_type == "remediation":
        for c in weak_concepts:
            advice.append(
                f"You repeatedly struggle with {c}. Revise fundamentals and solve easy problems first."
            )

    elif task_type == "onboarding":
        advice.append(
            "This seems like a new topic for you. Start with beginner explanations and examples."
        )

    else:
        advice.append("Practice similar questions again.")

    recommendation["advice"] = advice

    # -------- EXPLANATION METADATA --------
    recommendation["original_input"] = text
    recommendation["concept"] = concept
    recommendation["task_type"] = task_type
    recommendation["agents_used"] = [
        "Memory Agent",
        "Pattern Agent",
        "Retrieval Agent",
        "Recommendation Agent",
    ]

    return recommendation
