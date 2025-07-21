
"""
JARVIS Configuration Settings
"""
import os
from typing import Dict, Any

class JarvisConfig:
    # API Configuration
    GROQ_API_KEY = "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"
    GROQ_MODEL = "llama2-70b-4096"
    MAX_TOKENS = 500
    TEMPERATURE = 0.7
    
    # UI Configuration
    APP_TITLE = "JARVIS AI Assistant"
    APP_ICON = "🤖"
    THEME_COLOR = "#00ffff"
    BACKGROUND_COLOR = "#0a0a0a"
    
    # Animation Settings
    ENABLE_ANIMATIONS = True
    ARC_REACTOR_SPEED = 2.0
    PULSE_DURATION = 1.5
    
    # Chat Settings
    MAX_CONVERSATION_HISTORY = 10
    RESPONSE_TIMEOUT = 30
    ENABLE_SOUND = True
    
    # UI Colors (Iron Man Theme)
    COLORS = {
        'primary': '#00ffff',      # Cyan
        'secondary': '#ff6b35',    # Orange
        'accent': '#ffd700',       # Gold
        'background': '#0a0a0a',   # Dark
        'surface': '#1a1a1a',      # Darker
        'text': '#ffffff',         # White
        'success': '#00ff41',      # Green
        'warning': '#ff9800',      # Amber
        'error': '#ff5722',        # Red
        'arc_reactor': '#87ceeb',  # Sky Blue
    }
    
    # Gradients
    GRADIENTS = {
        'main': 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%)',
        'chat': 'linear-gradient(45deg, rgba(0,255,255,0.1) 0%, rgba(255,107,53,0.1) 100%)',
        'sidebar': 'linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%)',
        'button': 'linear-gradient(45deg, #00ffff 0%, #ff6b35 100%)',
        'arc_reactor': 'radial-gradient(circle, #87ceeb 0%, #00ffff 50%, #0066cc 100%)',
    }
