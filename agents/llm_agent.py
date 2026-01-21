import requests
from config import GEMINI_API_KEY, GEMINI_MODEL


GEMINI_URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def generate_explanation(user_text, weak_concepts, resources, task_type):

    if not GEMINI_API_KEY:
        return (
            "AI explanation unavailable: GEMINI_API_KEY is not set. "
            "Set it in your environment or a .env file."
        )

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
    url = f"{GEMINI_URL_BASE}/{GEMINI_MODEL}:generateContent"

    try:
        print(f"🔵 Calling Gemini API ({GEMINI_MODEL})...")

        res = requests.post(url, params=params, json=payload, timeout=30)
        if not res.ok:
            try:
                error_payload = res.json()
            except Exception:
                error_payload = res.text

            print("🔴 Gemini API HTTP error:", error_payload)
            return (
                "AI explanation unavailable: Gemini API request failed. "
                "Verify GEMINI_API_KEY and GEMINI_MODEL."
            )

        data = res.json()
        print("🟢 Gemini response received")

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.RequestException as e:
        print("🔴 Gemini API error:", e)
        return "AI explanation temporarily unavailable. Please rely on agent recommendations above."
