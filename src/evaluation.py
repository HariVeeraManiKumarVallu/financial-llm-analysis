def evaluate_llm_output(text):
    """
    Simple evaluation placeholder.
    In real systems this would measure relevance,
    factual grounding, etc.
    """

    score = 0

    if "risk" in text.lower():
        score += 1

    if "sector" in text.lower():
        score += 1

    if "return" in text.lower():
        score += 1

    return {"relevance_score": score}