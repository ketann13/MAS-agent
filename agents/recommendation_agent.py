def generate_recommendation(weak_concepts, resources, memory_events):
    rec = {}

    rec["weak_concepts"] = weak_concepts
    rec["similar_mistakes"] = memory_events
    rec["resources"] = resources

    advice = []
    for c in weak_concepts:
        advice.append(f"Revise concept: {c}")

    advice.append("Practice similar questions again.")

    rec["advice"] = advice
    return rec
