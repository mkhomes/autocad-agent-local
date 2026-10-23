import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "autocad-agent")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
PROJECTS_DIR = os.getenv("PROJECTS_DIR", "./projects")
AUTO_CAD_VISIBLE = os.getenv("AUTO_CAD_VISIBLE", "true").lower() == "true"
