import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")


def generate_explanation(user_text, weak_concepts, resources, task_type):
    resource_text = "\n".join([r["text"] for r in resources[:3]])

    prompt = f"""
You are an AI tutor helping a student.

Student doubt:
{user_text}

Weak concepts detected:
{", ".join(weak_concepts)}

Learning strategy selected by planner:
{task_type}

Relevant study material:
{resource_text}

Explain the concept clearly and give simple advice.
Do not change learning strategy. Just explain.
"""

    response = model.generate_content(prompt)
    return response.text
