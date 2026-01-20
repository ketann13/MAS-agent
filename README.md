# MAS Learning Agent

Skeleton structure for a multi-agent learning assistant with Qdrant backing. Fill in the placeholders to add real logic.

## Layout
- app.py: main entry (CLI/Streamlit later)
- embeddings.py: embedding model loader
- config.py: constants & settings
- qdrant_db/: Qdrant client and collection setup
- agents/: planner, memory, pattern, retrieval, recommendation agents
- services/: event logging and evaluation
- data/: sample resources and events
- scripts/: loaders for resources and events
- utils/: text utilities
