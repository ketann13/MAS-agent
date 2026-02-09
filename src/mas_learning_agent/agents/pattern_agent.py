from collections import Counter


def _normalize_concept(concept: str) -> str:
    return (concept or "").strip().lower()


def detect_weak_concepts(events, current_concept=None):
    """
    Detect weak concepts based on:
    - repeated mistakes
    - recent mistakes
    - current input priority
    """

    concepts = []

    # prioritize incorrect attempts
    for e in events:
        if not e.get("correct", False):
            concepts.append(_normalize_concept(e.get("concept")))

    # always prioritize current concept
    if current_concept:
        concepts.append(_normalize_concept(current_concept))

    if not concepts:
        return []

    counter = Counter(concepts)

    # return top 2 weak concepts
    weak_concepts = [c for c, _ in counter.most_common(2)]

    return weak_concepts
