import os
from dotenv import load_dotenv

LEARNING_EVENTS_COLLECTION = "learning_events"
LEARNING_RESOURCES_COLLECTION = "learning_resources"
FEEDBACK_LOGS_COLLECTION = "feedback_logs"
CONCEPT_STATS_COLLECTION = "concept_stats"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K_MEMORY = 3
TOP_K_RESOURCES = 3

# Load .env if present (override any existing env vars)
load_dotenv(override=True)

# Read from environment instead of hardcoding
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemma-3-4b-it")
