from state_builder import build_state

from intent_classifier import (
    classify_intent
)


messages = [

    {
        "role": "user",
        "content": (
            "Hiring a Java developer"
        )
    },

    {
        "role": "assistant",
        "content": (
            "What seniority level?"
        )
    },

    {
        "role": "user",
        "content": (
            "Mid-level around 4 years"
        )
    },

    {
        "role": "user",
        "content": (
            "Also include personality tests"
        )
    }
]


state = build_state(messages)

intent = classify_intent(
    messages,
    state
)


print(state)

print(intent)