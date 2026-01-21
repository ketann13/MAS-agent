import requests
from mas_learning_agent.config import GEMINI_API_KEY


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-flash-latest:generateContent"
)


def generate_explanation(user_text, weak_concepts, resources, task_type):

    resource_text = "\n".join([r["text"] for r in resources[:3]])

    prompt = f"""
You are an AI tutor.

Student doubt:
{user_text}

Weak concepts:
{", ".join(weak_concepts)}

Learning strategy decided by agents:
{task_type}

Relevant study material:
{resource_text}

Explain clearly in simple words and give advice.
Do not change learning strategy.
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    params = {"key": GEMINI_API_KEY}

    try:
        print("🔵 Calling Gemini API (flash-latest)...")

        res = requests.post(GEMINI_URL, params=params, json=payload, timeout=30)
        res.raise_for_status()

        data = res.json()
        print("🟢 Gemini response received")

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print("🔴 Gemini API error:", e)
        return "AI explanation temporarily unavailable. Please rely on agent recommendations above."
