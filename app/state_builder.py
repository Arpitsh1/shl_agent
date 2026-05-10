import re


SKILL_KEYWORDS = [
    "java",
    "python",
    "sql",
    "react",
    "javascript",
    "aws",
    "docker",
    "kubernetes",
    ".net",
    "spring",
    "django",
    "node",
    "angular"
]


SOFT_SKILLS = {
    "stakeholder": "communication",
    "communication": "communication",
    "leadership": "leadership",
    "teamwork": "teamwork",
    "client-facing": "client-facing",
    "presentation": "presentation",
    "collaboration": "collaboration"
}


PERSONALITY_TERMS = [
    "personality",
    "behavioral",
    "behavioural",
    "culture fit",
    "soft skills"
]


SENIORITY_PATTERNS = {
    "junior": [
        "junior",
        "entry level",
        "entry-level",
        "fresher",
        "graduate"
    ],

    "mid-level": [
        "mid-level",
        "mid level",
        "3 years",
        "4 years",
        "5 years",
        "intermediate"
    ],

    "senior": [
        "senior",
        "lead",
        "architect",
        "principal",
        "manager",
        "head"
    ]
}


ROLE_PATTERNS = {
    "software engineer": [
        "developer",
        "software engineer",
        "backend engineer",
        "frontend engineer",
        "full stack"
    ],

    "data analyst": [
        "data analyst",
        "analytics",
        "business intelligence"
    ],

    "sales": [
        "sales",
        "account manager",
        "business development"
    ]
}


def extract_seniority(text):

    for level, patterns in (
        SENIORITY_PATTERNS.items()
    ):

        for pattern in patterns:

            if pattern in text:
                return level

    return None


def extract_role(text):

    for role, patterns in (
        ROLE_PATTERNS.items()
    ):

        for pattern in patterns:

            if pattern in text:
                return role

    return None


def extract_skills(text):

    found = []

    for skill in SKILL_KEYWORDS:

        if skill in text:
            found.append(skill)

    return list(set(found))


def extract_soft_skills(text):

    found = []

    for key, value in SOFT_SKILLS.items():

        if key in text:
            found.append(value)

    return list(set(found))


def personality_requested(text):

    for term in PERSONALITY_TERMS:

        if term in text:
            return True

    return False


def detect_comparison(text):

    comparison_words = [
        "compare",
        "difference between",
        "vs",
        "versus"
    ]

    for word in comparison_words:

        if word in text:
            return True

    return False


def extract_comparison_items(text):

    patterns = [
        r"compare (.*?) and (.*?)$",
        r"difference between (.*?) and (.*?)$",
        r"(.*?) vs (.*?)$",
        r"(.*?) versus (.*?)$"
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:

            return [
                match.group(1).strip(),
                match.group(2).strip()
            ]

    return []


def build_state(messages):

    state = {

        "role": None,

        "seniority": None,

        "skills": [],

        "soft_skills": [],

        "personality_required": False,

        "technical_required": True,

        "comparison_requested": False,

        "comparison_items": [],

        "latest_user_message": ""
    }

    user_messages = []

    for message in messages:

        if message["role"] == "user":

            user_messages.append(
                message["content"].lower()
            )

    full_text = " ".join(user_messages)

    state["latest_user_message"] = (
        user_messages[-1]
        if user_messages
        else ""
    )

    state["role"] = extract_role(
        full_text
    )

    state["seniority"] = extract_seniority(
        full_text
    )

    state["skills"] = extract_skills(
        full_text
    )

    state["soft_skills"] = (
        extract_soft_skills(full_text)
    )

    state["personality_required"] = (
        personality_requested(full_text)
    )

    state["comparison_requested"] = (
        detect_comparison(full_text)
    )

    if state["comparison_requested"]:

        state["comparison_items"] = (
            extract_comparison_items(
                full_text
            )
        )

    return state