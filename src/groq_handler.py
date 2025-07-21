

"""
Groq API Handler - Manages AI responses
"""
import streamlit as st
from groq import Groq
import datetime
from typing import List, Dict, Any, Optional
from config import JarvisConfig

class GroqHandler:
    """Handles all Groq API interactions"""
    
    def __init__(self):
        self.client: Optional[Groq] = None
        self.api_connected: bool = False
        self.connection_error: Optional[str] = None
        self.model: str = JarvisConfig.GROQ_MODEL
        self.request_count: int = 0
        self.last_request_time: Optional[datetime.datetime] = None
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Groq client"""
        try:
            # Get API key
            api_key = self._get_api_key()
            
            if not api_key:
                raise ValueError("No API key found")
            
            # Create client
            self.client = Groq(api_key=api_key)
            
            # Test connection
            self._test_connection()
            
            self.api_connected = True
            self.connection_error = None
            
        except Exception as e:
            self.api_connected = False
            self.connection_error = str(e)
            st.error(f"❌ Groq API Error: {self.connection_error}")
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from various sources"""
        # Try Streamlit secrets first
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
            if api_key and len(api_key) > 20:
                return api_key
        except:
            pass
        
        # Fallback to config
        api_key = JarvisConfig.GROQ_API_KEY
        if api_key and len(api_key) > 20:
            return api_key
        
        return None
    
    def _test_connection(self):
        """Test API connection"""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model=self.model,
                max_tokens=5
            )
            return True
        except Exception as e:
            raise Exception(f"Connection test failed: {str(e)}")
    
    def get_response(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """Get AI response from Groq"""
        if not self.api_connected or not self.client:
            return f"🔧 I'm not connected to my AI brain. Error: {self.connection_error}"
        
        try:
            self.request_count += 1
            self.last_request_time = datetime.datetime.now()
            
            # Build system message
            system_message = """You are JARVIS, Tony Stark's advanced AI assistant from Iron Man. 

Your personality:
- Highly intelligent and sophisticated
- Professional yet witty
- Slight British accent in your responses
- Confident and capable
- Loyal and helpful
- Technical expertise in all fields
- Always address user respectfully

Your capabilities:
- Answer complex questions with accuracy
- Explain technology in simple terms
- Provide creative solutions
- Engage in meaningful conversations
- Assist with problem-solving

Keep responses:
- Clear and informative
- Conversational but professional
- Under 300 words unless specifically requested otherwise
- Engaging and helpful"""

            # Build messages
            messages = [{"role": "system", "content": system_message}]
            
            # Add conversation history
            if conversation_history:
                for conv in conversation_history[-3:]:  # Last 3 exchanges
                    messages.append({"role": "user", "content": conv.get('user', '')})
                    messages.append({"role": "assistant", "content": conv.get('assistant', '')})
            
            # Add current query
            messages.append({"role": "user", "content": user_input})
            
            # Make API call
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=JarvisConfig.MAX_TOKENS,
                temperature=JarvisConfig.TEMPERATURE
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I'm experiencing technical difficulties: {str(e)}"
    
    def get_status(self) -> Dict[str, Any]:
        """Get handler status"""
        return {
            'connected': self.api_connected,
            'model': self.model,
            'requests_made': self.request_count,
            'last_request': self.last_request_time.strftime('%H:%M:%S') if self.last_request_time else 'Never',
            'error': self.connection_error
        }
