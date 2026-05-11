from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.schemas import (
    ChatRequest,
    ChatResponse
)

from app.state_builder import (
    build_state
)

from app.intent_classifier import (
    classify_intent
)

from app.retriever import (
    retrieve_assessments
)

from app.comparison import (
    compare_assessments
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(req: ChatRequest):

    try:

        messages = [
            m.dict()
            for m in req.messages
        ]

        # reconstruct state
        state = build_state(
            messages
        )

        # classify intent
        intent = classify_intent(
            messages,
            state
        )

        # refusal
        if intent == "refusal":

            return {

                "reply": (
                    "I can only discuss "
                    "SHL assessments and "
                    "related recommendation requests."
                ),

                "recommendations": [],

                "end_of_conversation": False
            }

        # clarification
        if intent == "clarification":

            return {

                "reply": (
                    "What role and seniority level "
                    "are you hiring for, and are "
                    "you mainly evaluating technical "
                    "skills, behavioral traits, or both?"
                ),

                "recommendations": [],

                "end_of_conversation": False
            }

        # comparison
        if intent == "comparison":

            items = state[
                "comparison_items"
            ]

            if len(items) < 2:

                return {

                    "reply": (
                        "Please specify two SHL "
                        "assessments to compare."
                    ),

                    "recommendations": [],

                    "end_of_conversation": False
                }

            comparison_text = (
                compare_assessments(
                    items[0],
                    items[1]
                )
            )

            return {

                "reply": comparison_text,

                "recommendations": [],

                "end_of_conversation": False
            }

        # recommendation
        recommendations = (
            retrieve_assessments(
                state["latest_user_message"],
                top_k=10
                )
            )

        formatted = []

        for r in recommendations:

            formatted.append({

                "name": r["name"],

                "url": r["url"],

                "test_type": (
                    r.get(
                        "test_type",
                        "Unknown"
                    )
                )
            })

        reply = (
            f"I found {len(formatted)} "
            f"SHL assessments matching "
            f"your role, skills, and "
            f"evaluation requirements."
        )

        return {

            "reply": reply,

            "recommendations": formatted,

            "end_of_conversation": True
        }

    except Exception as e:

        print(e)

        return {

            "reply": (
                "An internal error occurred."
            ),

            "recommendations": [],

            "end_of_conversation": False
        }