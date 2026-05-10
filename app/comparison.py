import json

from app.llm import ask_llm


DATA_FILE = "data/assessments.json"


with open(
    DATA_FILE,
    "r",
    encoding="utf-8"
) as f:

    assessments = json.load(f)


def find_assessment(name):

    name = name.lower()

    for assessment in assessments:

        if name in assessment["name"].lower():

            return assessment

    return None


def compare_assessments(
    item_a,
    item_b
):

    assessment_a = find_assessment(
        item_a
    )

    assessment_b = find_assessment(
        item_b
    )

    if not assessment_a:

        return (
            f"I could not find "
            f"{item_a} in the SHL catalog."
        )

    if not assessment_b:

        return (
            f"I could not find "
            f"{item_b} in the SHL catalog."
        )

    prompt = f"""
You are an SHL assessment assistant.

Compare these two assessments STRICTLY using provided catalog information.

Assessment A:
{assessment_a}

Assessment B:
{assessment_b}

Focus on:
- purpose
- skills measured
- use case
- test type

Do not invent information.
"""

    return ask_llm(prompt)