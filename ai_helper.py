"""
ai_helper.py
------------
All communication with the Google Gemini AI API lives here.
Every feature (explain, summarize, code explainer, quiz) calls
one of the functions below.

HOW IT WORKS:
  1. We load the API key from the .env file (never hardcoded).
  2. We build a clear text prompt for each feature.
  3. We send the prompt to Gemini and return the response text.

NOTE: Uses the new `google-genai` SDK (google.genai), not the deprecated
      `google-generativeai` package.
"""

import os
from google import genai
from dotenv import load_dotenv

# ── Load environment variables from the .env file ──────────────────────────
load_dotenv()

# ── Read the API key from the environment ──────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model to use — gemini-2.0-flash is fast and available on the free tier
_MODEL = "gemini-2.0-flash"


def _get_client() -> genai.Client:
    """
    Build and return a Gemini Client.
    Raises a clear error if the API key is missing.
    """
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not set.\n"
            "Please add it to your .env file.  "
            "See .env.example for instructions."
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def explain_topic(topic: str) -> str:
    """
    Feature 1 — Explain a difficult topic in simple English.

    Args:
        topic: The subject or concept the student wants to understand.

    Returns:
        A beginner-friendly explanation as a string.
    """
    client = _get_client()
    prompt = (
        f"You are a friendly tutor explaining to a complete beginner.\n"
        f"Explain the following topic in simple, clear English. "
        f"Use everyday analogies where possible. "
        f"Keep the explanation under 300 words and use bullet points.\n\n"
        f"Topic: {topic}"
    )
    response = client.models.generate_content(model=_MODEL, contents=prompt)
    return response.text


def summarize_notes(notes: str) -> str:
    """
    Feature 2 — Summarize study notes pasted by the student.

    Args:
        notes: Raw study notes text pasted by the student.

    Returns:
        A concise summary with key points highlighted.
    """
    client = _get_client()
    prompt = (
        f"You are a study assistant. Read the following notes and produce:\n"
        f"1. A short summary (3-5 sentences).\n"
        f"2. A bullet list of the most important key points.\n"
        f"3. Any terms that a beginner should look up.\n\n"
        f"Notes:\n{notes}"
    )
    response = client.models.generate_content(model=_MODEL, contents=prompt)
    return response.text


def explain_code(code: str) -> str:
    """
    Feature 3 — Explain Python code line by line.

    Args:
        code: A snippet of Python code.

    Returns:
        A line-by-line explanation in plain English.
    """
    client = _get_client()
    prompt = (
        f"You are a Python tutor. Explain the following Python code "
        f"line by line in very simple English. "
        f"After the line-by-line explanation, add a short paragraph "
        f"describing what the overall code does.\n\n"
        f"```python\n{code}\n```"
    )
    response = client.models.generate_content(model=_MODEL, contents=prompt)
    return response.text


def generate_quiz(topic: str, num_questions: int = 5) -> str:
    """
    Feature 4 — Generate practice questions on any topic.

    Args:
        topic:         The topic to generate questions about.
        num_questions: How many questions to generate (default 5).

    Returns:
        A formatted quiz with multiple-choice questions and answers.
    """
    client = _get_client()
    prompt = (
        f"Create a practice quiz for a beginner student on the topic: '{topic}'.\n"
        f"Generate exactly {num_questions} multiple-choice questions.\n"
        f"Format each question like this:\n\n"
        f"Q1. [Question text]\n"
        f"   A) Option\n"
        f"   B) Option\n"
        f"   C) Option\n"
        f"   D) Option\n"
        f"Answer: [Correct option letter]\n\n"
        f"Keep the questions suitable for a beginner."
    )
    response = client.models.generate_content(model=_MODEL, contents=prompt)
    return response.text
