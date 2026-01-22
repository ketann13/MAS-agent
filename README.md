# RecallAI

RecallAI is an AI-powered personalized tutor with long-term memory. It uses a multi-agent workflow and Qdrant-backed retrieval to improve guidance over time.

## Layout
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
