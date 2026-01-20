from collections import Counter


def detect_weak_concepts(events):
    concepts = [e["concept"] for e in events if not e.get("correct", False)]
    counter = Counter(concepts)

    if not counter:
        return []

    return [c for c, _ in counter.most_common(2)]
