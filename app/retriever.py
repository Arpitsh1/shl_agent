import json
import re
from collections import Counter


DATA_FILE = "data/assessments.json"


with open(DATA_FILE, "r", encoding="utf-8") as f:
    assessments = json.load(f)


print("\n========== DATA DEBUG ==========")

print("TOTAL ASSESSMENTS:", len(assessments))

if len(assessments) > 0:

    print("\nFIRST ASSESSMENT SAMPLE:\n")

    print(assessments[0])

print("================================\n")


STOPWORDS = {
    "a",
    "an",
    "the",
    "for",
    "with",
    "and",
    "or",
    "to",
    "of",
    "in",
    "on",
    "need",
    "looking",
    "hire",
    "hiring",
    "developer",
    "assessment",
    "test",
    "someone",
    "person",
    "role",
    "job"
}


SYNONYMS = {

    "java": [
        "java",
        "core java",
        "java ee",
        "java frameworks",
        "java web services"
    ],

    "python": [
        "python"
    ],

    "frontend": [
        "frontend",
        "angular",
        "react",
        "javascript",
        "html",
        "css"
    ],

    "backend": [
        "backend",
        ".net",
        "api"
    ],

    "cloud": [
        "aws",
        "cloud",
        "docker",
        "kubernetes"
    ],

    "data": [
        "data science",
        "statistics",
        "analytics"
    ],

    "personality": [
        "opq",
        "personality",
        "behavioral"
    ],

    "cognitive": [
        "ability",
        "cognitive",
        "reasoning"
    ],

    "customer": [
        "customer service",
        "support",
        "call center"
    ]
}


CLARIFICATION_KEYWORDS = {
    "assessment",
    "test",
    "hire",
    "hiring",
    "role",
    "job"
}


TECH_KEYWORDS = {
    "java",
    "python",
    "aws",
    "cloud",
    "angular",
    "react",
    "javascript",
    "docker",
    "kubernetes",
    "data",
    "frontend",
    "backend",
    ".net",
    "sql",
    "linux"
}


PERSONALITY_KEYWORDS = {
    "personality",
    "behavioral",
    "leadership",
    "communication",
    "stakeholder",
    "teamwork"
}


COGNITIVE_KEYWORDS = {
    "cognitive",
    "reasoning",
    "aptitude",
    "problem solving",
    "analytical"
}


COMPARISON_WORDS = {
    "compare",
    "difference",
    "vs",
    "versus"
}


def clean_text(text):

    if not isinstance(text, str):

        text = str(text)

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s\.\+#]",
        " ",
        text
    )

    return text


def tokenize(text):

    text = clean_text(text)

    words = text.split()

    filtered = []

    for word in words:

        if word not in STOPWORDS:

            filtered.append(word)

    return filtered


def is_vague_query(message):

    tokens = tokenize(message)

    if len(tokens) <= 2:
        return True

    found_tech = any(
        token in TECH_KEYWORDS
        for token in tokens
    )

    found_personality = any(
        token in PERSONALITY_KEYWORDS
        for token in tokens
    )

    found_cognitive = any(
        token in COGNITIVE_KEYWORDS
        for token in tokens
    )

    if not (
        found_tech
        or found_personality
        or found_cognitive
    ):

        only_generic = all(
            token in CLARIFICATION_KEYWORDS
            for token in tokens
        )

        if only_generic:
            return True

    return False


def extract_keywords(message):

    tokens = tokenize(message)

    expanded_keywords = []

    for token in tokens:

        expanded_keywords.append(token)

        if token in SYNONYMS:

            expanded_keywords.extend(
                SYNONYMS[token]
            )

    return list(set(expanded_keywords))


def score_assessment(
    assessment,
    keywords
):

    score = 0

    print("\nASSESSMENT BEING SCORED:")

    print(assessment)

    searchable_text = " ".join([

        str(
            assessment.get(
                "name",
                ""
            )
        ),

        str(
            assessment.get(
                "description",
                ""
            )
        ),

        str(
            assessment.get(
                "test_type",
                ""
            )
        )

    ]).lower()

    print("SEARCHABLE TEXT:")

    print(searchable_text)

    for keyword in keywords:

        if keyword.lower() in searchable_text:

            score += 3

    keyword_counts = Counter(keywords)

    for keyword, count in keyword_counts.items():

        if keyword.lower() in searchable_text:

            score += count

    return score


def retrieve_assessments(query, top_k=10):

    keywords = extract_keywords(query)

    print("=" * 50)
    print("QUERY:", query)
    print("KEYWORDS:", keywords)

    scored = []

    for assessment in assessments:

        searchable_text = " ".join([
            assessment.get("name", ""),
            assessment.get("description", ""),
            assessment.get("test_type", ""),
            " ".join(assessment.get("keywords", []))
        ]).lower()

        score = 0

        # strong exact keyword matching
        for keyword in keywords:

            keyword = keyword.lower()

            if keyword in searchable_text:
                score += 10

        # prioritize exact java matches
        if "java" in keywords:

            if "java" in searchable_text:
                score += 30
            else:
                score -= 20

        # penalize irrelevant tech
        irrelevant_terms = [
            ".net",
            "accounting",
            "sales",
            "bank",
            "communication"
        ]

        for term in irrelevant_terms:

            if term in searchable_text and "java" in keywords:
                score -= 15

        # skip low relevance
        if score <= 0:
            continue

        scored.append((score, assessment))

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    print("FINAL RESULTS:", len(scored))
    print("=" * 50)

    results = []

    for score, assessment in scored[:top_k]:

        results.append({

            "name": assessment.get("name", ""),
            "url": assessment.get("url", ""),
            "test_type": assessment.get(
                "test_type",
                "Unknown"
            ),
            "description": assessment.get(
                "description",
                ""
            ),
            "score": score
        })

    return results

def detect_comparison_request(message):

    lower = message.lower()

    return any(
        word in lower
        for word in COMPARISON_WORDS
    )


def build_catalog_context(results):

    context = []

    for item in results:

        block = f"""
Name: {item.get('name', '')}
Type: {item.get('test_type', '')}
URL: {item.get('url', '')}
Description: {item.get('description', '')}
"""

        context.append(block)

    return "\n".join(context)