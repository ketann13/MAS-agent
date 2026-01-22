# RecallAI – Multi-Agent Personalized Learning Assistant

RecallAI is an AI-powered personalized tutor with long-term memory. It uses a multi-agent workflow and Qdrant-backed retrieval to provide tailored learning guidance that improves over time.

## Project Overview
RecallAI captures learning mistakes and queries, stores them as embeddings, and retrieves relevant past events and resources to generate targeted recommendations and AI tutor explanations.

## Problem Statement
Learners often repeat mistakes because prior errors and context are not remembered. RecallAI solves this by maintaining long-term memory of learning events and using a multi-agent reasoning pipeline to personalize feedback and resources.

## Features
- Multi-agent pipeline: memory, pattern detection, retrieval, recommendation, and AI tutor agents
- Long-term vector memory with Qdrant
- Personalized remediation strategy based on user history
- Streamlit UI with transparent agent reasoning and feedback loop
- Feedback-driven learning to improve future guidance

## System Architecture (Multi-Agent)
1. **Memory Agent**: stores learning events and retrieves similar mistakes.
2. **Pattern Agent**: detects weak concepts from history and current input.
3. **Retrieval Agent**: fetches related resources from Qdrant.
4. **Recommendation Agent**: generates learning strategy and advice.
5. **LLM Tutor Agent**: provides natural-language explanations.

## Tech Stack
- **Frontend**: Streamlit
- **Vector DB**: Qdrant
- **Embeddings**: Sentence Transformers
- **LLM**: Google Gemini (via API)
- **Language**: Python

## How It Works (Step-by-step workflow)
1. User submits a learning issue and concept.
2. Memory Agent stores the event and retrieves similar past mistakes.
3. Pattern Agent identifies weak concepts.
4. Retrieval Agent gathers related resources.
5. Recommendation Agent chooses a learning strategy and advice.
6. LLM Tutor Agent generates a plain-language explanation.
7. User feedback is stored to improve future results.

## Local Setup Instructions
1. Create and activate a virtual environment.
2. Install dependencies:
	- `pip install -r requirements.txt`
3. Configure environment variables (see below).
4. Start the app:
	- `python -m streamlit run app/streamlit_app.py`

## Environment Variables
Create a `.env` file (do not commit) with:
- `QDRANT_URL`
- `QDRANT_API_KEY`
- `GEMINI_API_KEY`
- `GEMINI_MODEL` (optional)

## Project Structure
- app/streamlit_app.py: Streamlit entry
- src/mas_learning_agent/: application package
  - config.py: constants & settings
  - embeddings.py: embedding model loader
  - agents/: planner, memory, pattern, retrieval, recommendation agents
  - qdrant_db/: Qdrant client and collection setup
  - services/: event logging and evaluation
  - utils/: text utilities
- data/: sample resources and events
- scripts/: loaders for resources and events
- .streamlit/: Streamlit config

## Author
- Ketan N.
