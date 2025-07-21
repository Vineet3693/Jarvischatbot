
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Groq API (FREE)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # App settings
    APP_TITLE = "JARVIS AI Assistant"
    APP_ICON = "🤖"
    
    # Model settings
    DEFAULT_MODEL = "llama2-70b-4096"
    MAX_TOKENS = 500
    TEMPERATURE = 0.7
    
    # Cache settings
    ENABLE_CACHE = True
    CACHE_TTL = 3600  # 1 hour
    
    # Response settings
    MAX_HISTORY = 10
    RESPONSE_TIMEOUT = 30
