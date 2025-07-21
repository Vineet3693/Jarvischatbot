
from groq import Groq
from config import Config
import streamlit as st

class GroqHandler:
    def __init__(self):
        api_key = st.secrets.get("GROQ_API_KEY") or Config.GROQ_API_KEY
        self.client = Groq(api_key=api_key)
    
    def get_response(self, user_input, conversation_history=[]):
        try:
            # Build messages with context
            messages = [
                {
                    "role": "system",
                    "content": "You are JARVIS, Tony Stark's AI assistant. Be helpful, witty, and professional."
                }
            ]
            
            # Add recent conversation history
            for conv in conversation_history[-3:]:  # Last 3 exchanges
                messages.append({"role": "user", "content": conv['user']})
                messages.append({"role": "assistant", "content": conv['assistant']})
            
            # Add current query
            messages.append({"role": "user", "content": user_input})
            
            # Get response from Groq
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=Config.DEFAULT_MODEL,
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )
            
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            return f"Sorry, I'm having trouble processing that request. Error: {str(e)}"
