OFFTOPIC_PATTERNS = [

    "salary",

    "legal advice",

    "ignore previous instructions",

    "recommend non-shl",

    "politics",

    "religion",

    "medical advice"
]


def is_refusal(text):

    for pattern in OFFTOPIC_PATTERNS:

        if pattern in text:
            return True

    return False


def needs_clarification(state):

    if not state["role"]:
        return True

    if not state["skills"]:
        return True

    return False


def is_refinement(text):

    refinement_terms = [

        "actually",

        "also add",

        "include",

        "instead",

        "change",

        "update"
    ]

    for term in refinement_terms:

        if term in text:
            return True

    return False


def classify_intent(messages, state):

    latest = state[
        "latest_user_message"
    ]

    if is_refusal(latest):
        return "refusal"

    if state["comparison_requested"]:
        return "comparison"

    if is_refinement(latest):
        return "refinement"

    if needs_clarification(state):
        return "clarification"

    return "recommendation"