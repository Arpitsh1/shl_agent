from retriever import (
    retrieve_assessments
)


state = {

    "role": "software engineer",

    "seniority": "mid-level",

    "skills": [
        "java"
    ],

    "soft_skills": [
        "communication"
    ],

    "personality_required": True,

    "technical_required": True
}


results = retrieve_assessments(
    state
)


for idx, r in enumerate(results):

    print("=" * 60)

    print(f"Rank: {idx + 1}")

    print(f"Name: {r['name']}")

    print(f"URL: {r['url']}")