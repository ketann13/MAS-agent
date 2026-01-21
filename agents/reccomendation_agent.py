def generate_recommendation(weak_concepts, resources, memory_events, task_type):

    advice = []

    if task_type == "remediation":
        for c in weak_concepts:
            advice.append(
                f"You repeatedly struggle with {c}. Revise fundamentals and solve easy problems."
            )

    elif task_type == "onboarding":
        advice.append(
            "This seems like a new topic for you. Start with beginner explanations and examples."
        )

    else:  # practice
        advice.append("Practice similar questions to strengthen this concept.")

    # Resource-aware advice
    if resources:
        advice.append("Use the recommended explanations above before solving problems.")
    else:
        advice.append("No stored resources found. Rely on AI tutor explanation.")

    return advice
