from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "Gemini Web Search")
MODEL_ID = os.getenv("MODEL_ID", "gemini-2.5-flash")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
SYSTEM_INSTRUCTION = os.getenv("SYSTEM_INSTRUCTION", "You are a professional assistant. Be concise, accurate, and helpful.")
MODEL_OPTIONS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-3-flash-preview", "gemini-3-pro-preview"]