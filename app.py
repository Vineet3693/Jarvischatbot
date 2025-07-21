
import streamlit as st
import datetime
import random
from groq import Groq

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
        """Classify user input intent"""
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
        """Get appropriate built-in response"""
        if intent == 'time':
            return self._get_current_time()
        elif intent == 'date':
            return self._get_current_date()
        elif intent in self.responses:
            return random.choice(self.responses[intent])
        else:
            return "I'm processing your request. Please wait a moment."
    
    def _get_current_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        time_str = now.strftime('%I:%M %p')
        return f"The current time is {time_str}, sir."
    
    def _get_current_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        date_str = now.strftime('%A, %B %d, %Y')
        return f"Today is {date_str}."

class GroqHandler:
    def __init__(self):
        """Initialize Groq client with API key"""
        self.client = None
        self.api_connected = False
        
        try:
            # Try to get API key from Streamlit secrets first
            api_key = None
            
            try:
                api_key = st.secrets["GROQ_API_KEY"]
                st.sidebar.info("🔑 Using API key from Streamlit secrets")
            except:
                # Fallback: Use the key temporarily (ONLY FOR TESTING)
                # ⚠️ Replace this with your NEW key after revoking the old one
                api_key = "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"
                st.sidebar.warning("⚠️ Using hardcoded API key (not recommended)")
            
            if not api_key or len(api_key) < 10:
                raise ValueError("Invalid or missing API key")
            
            # Initialize Groq client
            self.client = Groq(api_key=api_key)
            self.model = "llama2-70b-4096"
            
            # Test connection
            self._test_connection()
            self.api_connected = True
            
        except Exception as e:
            st.sidebar.error(f"❌ Groq API Error: {str(e)}")
            self.client = None
            self.api_connected = False
    
    def _test_connection(self):
        """Test API connection"""
        try:
            test_response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "Hi"}],
                model=self.model,
                max_tokens=5
            )
            st.sidebar.success("✅ Groq API Connected!")
            return True
        except Exception as e:
            raise Exception(f"API test failed: {str(e)}")
    
    def get_response(self, user_input, conversation_history=[]):
        """Get AI response from Groq"""
        if not self.client or not self.api_connected:
            return "❌ I'm not connected to my AI brain. Please check the API configuration."
        
        try:
            # Build messages with context
            messages = [
                {
                    "role": "system",
                    "content": """You are JARVIS, Tony Stark's AI assistant from Iron Man. 
                    You are helpful, intelligent, witty, and professional. 
                    You have a slight British accent in your tone.
                    You're great at explaining technology and complex topics in simple terms.
                    Keep responses conversational but informative.
                    Address the user respectfully."""
                }
            ]
            
            # Add conversation history for context
            for conv in conversation_history[-3:]:
                messages.append({"role": "user", "content": conv['user']})
                messages.append({"role": "assistant", "content": conv['assistant']})
            
            # Add current query
            messages.append({"role": "user", "content": user_input})
            
            # Make API call to Groq
            with st.spinner("JARVIS is thinking..."):
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model=self.model,
                    max_tokens=500,
                    temperature=0.7,
                    top_p=1,
                    stream=False
                )
            
            response = chat_completion.choices[0].message.content
            return response
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties: {str(e)}"

class JarvisBrain:
    def __init__(self):
        self.groq = GroqHandler()
        self.builtin = BuiltinResponses()
        self.classifier = IntentClassifier()
        self.conversation_history = []
    
    def process_query(self, user_input):
        """Main query processing method"""
        try:
            user_input = user_input.strip()
            if not user_input:
                return "I didn't receive any input. Please ask me something!"
            
            # Classify intent
            intent = self.classifier.classify(user_input)
            
            # Route to appropriate handler
            if intent in ['time', 'date', 'greeting', 'simple']:
                response = self.builtin.get_response(user_input, intent)
            else:
                response = self.groq.get_response(user_input, self.conversation_history)
            
            # Update conversation history
            self.conversation_history.append({
                'user': user_input,
                'assistant': response,
                'intent': intent
            })
            
            # Keep only last 10 exchanges
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return self._format_response(response)
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def _format_response(self, response):
        """Format response for better display"""
        if not response:
            return "I apologize, but I couldn't generate a proper response."
        
        response = response.strip()
        
        if not response.endswith(('.', '!', '?', ':')):
            response += '.'
        
        return response

def main():
    # Initialize JARVIS in session state
    if 'jarvis' not in st.session_state:
        st.session_state.jarvis = JarvisBrain()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Title and description
    st.title("🤖 JARVIS AI Assistant")
    st.markdown("*Just A Rather Very Intelligent System*")
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ JARVIS Controls")
        
        # API Status
        st.subheader("📡 System Status")
        
        # Show API key status
        try:
            if hasattr(st.session_state.jarvis.groq, 'api_connected') and st.session_state.jarvis.groq.api_connected:
                st.success("✅ AI Brain Online")
                st.info("🧠 Powered by Groq Llama 2")
            else:
                st.error("❌ AI Brain Offline")
        except:
            st.warning("⚠️ Checking AI connection...")
        
        # Message count
        st.metric("💬 Conversation", len(st.session_state.messages))
        
        # Clear chat
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.jarvis.conversation_history = []
            st.success("Chat cleared!")
            st.rerun()
        
        # Quick commands
        st.subheader("⚡ Quick Commands")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👋 Hello", use_container_width=True):
                st.session_state.quick_query = "Hello JARVIS"
            
            if st.button("⏰ Time", use_container_width=True):
                st.session_state.quick_query = "What time is it?"
        
        with col2:
            if st.button("🤖 About AI", use_container_width=True):
                st.session_state.quick_query = "What is artificial intelligence?"
            
            if st.button("🔬 Explain Tech", use_container_width=True):
                st.session_state.quick_query = "How do computers work?"
        
        # Usage info
        st.subheader("📊 Usage Info")
        st.info("Free tier: 100k tokens/day")
        st.caption("Powered by Groq's lightning-fast inference")
    
    # Main chat interface
    st.subheader("💬 Chat with JARVIS")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle quick queries
    if hasattr(st.session_state, 'quick_query'):
        prompt = st.session_state.quick_query
        del st.session_state.quick_query
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get JARVIS response
        with st.chat_message("assistant"):
            response = st.session_state.jarvis.process_query(prompt)
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask JARVIS anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get JARVIS response
        with st.chat_message("assistant"):
            response = st.session_state.jarvis.process_query(prompt)
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
