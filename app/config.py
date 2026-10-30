import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
