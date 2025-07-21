
import streamlit as st
import datetime
import random
from groq import Groq
import os

# Page configuration
st.set_page_config(
    page_title="JARVIS AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for JARVIS theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0c0c0c, #1a1a1a);
        color: #00ffff;
    }
    .stChatMessage {
        background-color: rgba(0, 255, 255, 0.1);
        border: 1px solid #00ffff;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .stSidebar {
        background-color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

class IntentClassifier:
    def __init__(self):
        self.intent_keywords = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'time': ['time', 'clock', 'what time is it', 'current time'],
            'date': ['date', 'today', 'what day', 'current date', 'what date'],
            'simple': ['ok', 'okay', 'yes', 'no', 'thanks', 'thank you', 'bye', 'goodbye']
        }
    
    def classify(self, user_input):
        user_input_lower = user_input.lower().strip()
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    return intent
        return 'complex'

class BuiltinResponses:
    def __init__(self):
        self.responses = {
            'greeting': [
                "Hello! I'm JARVIS, your AI assistant. How may I assist you today?",
                "Good day! JARVIS here, ready to help with whatever you need.",
                "Greetings! I'm at your service. What can I do for you?",
                "Hello there! JARVIS reporting for duty. How can I help?"
            ],
            'simple': [
                "Understood. Is there anything else you'd like to know?",
                "I see. What else would you like to explore?",
                "Got it! How else may I assist you?",
                "Very well. What other questions do you have?"
            ]
        }
    
    def get_response(self, user_input, intent):
        if intent == 'time':
            return self._get_current_time()
        elif intent == 'date':
            return self._get_current_date()
        elif intent in self.responses:
            return random.choice(self.responses[intent])
        else:
            return "I'm processing your request. Please wait a moment."
    
    def _get_current_time(self):
        now = datetime.datetime.now()
        time_str = now.strftime('%I:%M %p')
        return f"The current time is {time_str}, sir."
    
    def _get_current_date(self):
        now = datetime.datetime.now()
        date_str = now.strftime('%A, %B %d, %Y')
        return f"Today is {date_str}."

class GroqHandler:
    def __init__(self):
        self.client = None
        self.api_connected = False
        self.connection_error = None
        
        # Get API key
        api_key = self._get_api_key()
        
        if api_key:
            try:
                # Initialize Groq client (simplified - no extra parameters)
                self.client = Groq(api_key=api_key)
                self.model = "llama2-70b-4096"
                
                # Test the connection
                self._test_connection()
                self.api_connected = True
                st.sidebar.success("✅ Groq API Connected!")
                
            except Exception as e:
                self.connection_error = f"Client initialization failed: {str(e)}"
                self.api_connected = False
                st.sidebar.error(f"❌ Connection Error: {str(e)}")
        else:
            self.connection_error = "No valid API key found"
            self.api_connected = False
            st.sidebar.error("❌ No API key found")
    
    def _get_api_key(self):
        """Get API key from multiple sources"""
        # Method 1: Streamlit secrets (recommended)
        try:
            api_key = st.secrets["GROQ_API_KEY"]
            if api_key and len(api_key) > 20:
                st.sidebar.info("🔑 Using key from Streamlit secrets")
                return api_key
        except Exception as e:
            st.sidebar.warning(f"Secrets not found: {str(e)}")
        
        # Method 2: Environment variable
        try:
            api_key = os.environ.get("GROQ_API_KEY")
            if api_key and len(api_key) > 20:
                st.sidebar.info("🔑 Using key from environment")
                return api_key
        except:
            pass
        
        # Method 3: Temporary fallback (REPLACE THIS WITH YOUR NEW KEY!)
        # ⚠️ Remember to create a NEW key since the old one was exposed!
        api_key = "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"
        
        if api_key and len(api_key) > 20:
            st.sidebar.warning("⚠️ Using hardcoded key (not secure)")
            return api_key
        
        return None
    
    def _test_connection(self):
        """Test API connection with minimal parameters"""
        try:
            # Simple test call
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model=self.model,
                max_tokens=5
            )
            return True
        except Exception as e:
            raise Exception(f"API test failed: {str(e)}")
    
    def get_response(self, user_input, conversation_history=[]):
        """Get AI response from Groq"""
        if not self.api_connected or not self.client:
            return f"🔧 I'm not connected to my AI brain. Error: {self.connection_error}"
        
        try:
            # Build messages
            messages = [
                {
                    "role": "system",
                    "content": """You are JARVIS, Tony Stark's AI assistant. You are helpful, intelligent, witty, and professional. Keep responses clear and informative."""
                }
            ]
            
            # Add conversation context (last 2 exchanges)
            for conv in conversation_history[-2:]:
                messages.append({"role": "user", "content": conv['user']})
                messages.append({"role": "assistant", "content": conv['assistant']})
            
            # Add current query
            messages.append({"role": "user", "content": user_input})
            
            # Make API call with minimal parameters
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I'm experiencing technical difficulties: {str(e)}"

class JarvisBrain:
    def __init__(self):
        self.groq = GroqHandler()
        self.builtin = BuiltinResponses()
        self.classifier = IntentClassifier()
        self.conversation_history = []
    
    def process_query(self, user_input):
        try:
            user_input = user_input.strip()
            if not user_input:
                return "I didn't receive any input. Please ask me something!"
            
            # Classify intent
            intent = self.classifier.classify(user_input)
            
            # Route to handler
            if intent in ['time', 'date', 'greeting', 'simple']:
                response = self.builtin.get_response(user_input, intent)
            else:
                response = self.groq.get_response(user_input, self.conversation_history)
            
            # Update history
            self.conversation_history.append({
                'user': user_input,
                'assistant': response,
                'intent': intent
            })
            
            # Keep last 8 exchanges
            if len(self.conversation_history) > 8:
                self.conversation_history = self.conversation_history[-8:]
            
            return response
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"

def main():
    # Initialize JARVIS
    if 'jarvis' not in st.session_state:
        st.session_state.jarvis = JarvisBrain()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Title
    st.title("🤖 JARVIS AI Assistant")
    st.markdown("*Just A Rather Very Intelligent System*")
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ JARVIS Controls")
        
        # System status
        st.subheader("📡 System Status")
        
        # Show connection status
        if hasattr(st.session_state.jarvis.groq, 'api_connected'):
            if st.session_state.jarvis.groq.api_connected:
                st.success("✅ AI Brain Online")
                st.info("🧠 Groq Llama 2 Ready")
            else:
                st.error("❌ AI Brain Offline")
        
        # Message count
        st.metric("💬 Messages", len(st.session_state.messages))
        
        # Controls
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.jarvis.conversation_history = []
            st.rerun()
        
        # Quick tests
        st.subheader("⚡ Quick Commands")
        
        if st.button("👋 Hello", use_container_width=True):
            st.session_state.quick_query = "Hello JARVIS"
        
        if st.button("⏰ Time", use_container_width=True):
            st.session_state.quick_query = "What time is it?"
            
        if st.button("🤖 About AI", use_container_width=True):
            st.session_state.quick_query = "What is artificial intelligence?"
        
        # Debug section
        with st.expander("🔧 Debug Info"):
            if st.button("Test Connection"):
                try:
                    api_key = st.session_state.jarvis.groq._get_api_key()
                    if api_key:
                        st.success(f"Key found: {api_key[:15]}...")
                        # Test client creation
                        test_client = Groq(api_key=api_key)
                        st.success("✅ Client created successfully!")
                    else:
                        st.error("❌ No API key found")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Main chat interface
    st.subheader("💬 Chat with JARVIS")
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle quick queries
    if hasattr(st.session_state, 'quick_query'):
        prompt = st.session_state.quick_query
        del st.session_state.quick_query
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("JARVIS is thinking..."):
                response = st.session_state.jarvis.process_query(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask JARVIS anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("JARVIS is thinking..."):
                response = st.session_state.jarvis.process_query(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
