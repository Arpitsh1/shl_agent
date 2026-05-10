import os

import google.generativeai as genai

from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


genai.configure(
    api_key=API_KEY
)


model = genai.GenerativeModel(
    "gemini-1.5-flash"
)


SYSTEM_PROMPT = """
You are an SHL assessment recommendation assistant.

Rules:
- Only discuss SHL assessments.
- Never invent assessments.
- Never invent URLs.
- Keep responses concise.
- Stay grounded in provided catalog data.
"""


def ask_llm(prompt):

    response = model.generate_content(

        SYSTEM_PROMPT +

        "\n\n" +

        prompt
    )

    return response.text.strip()