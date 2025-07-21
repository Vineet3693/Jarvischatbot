
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
        
        # Check for exact matches first
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    return intent
        
        # If no simple intent found, it's complex (goes to AI)
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
        """Initialize Groq client with API key from Streamlit secrets"""
        try:
            # Get API key from Streamlit secrets
            api_key = st.secrets["GROQ_API_KEY"]
            
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in secrets")
            
            # Initialize Groq client
            self.client = Groq(api_key=api_key)
            self.model = "llama2-70b-4096"  # Free model
            
        except Exception as e:
            st.error(f"Failed to initialize Groq API: {str(e)}")
            self.client = None
    
    def get_response(self, user_input, conversation_history=[]):
        """Get AI response from Groq"""
        if not self.client:
            return "Sorry, I'm having trouble connecting to my AI brain. Please check the API configuration."
        
        try:
            # Build messages with context
            messages = [
                {
                    "role": "system",
                    "content": """You are JARVIS, Tony Stark's AI assistant from Iron Man. 
                    You are helpful, intelligent, witty, and professional. 
                    You have a slight British accent in your tone.
                    You're great at explaining technology and complex topics in simple terms.
                    Keep responses conversational but informative."""
                }
            ]
            
            # Add recent conversation history for context
            for conv in conversation_history[-3:]:  # Last 3 exchanges
                messages.append({"role": "user", "content": conv['user']})
                messages.append({"role": "assistant", "content": conv['assistant']})
            
            # Add current query
            messages.append({"role": "user", "content": user_input})
            
            # Make API call to Groq
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=500,
                temperature=0.7,
                top_p=1,
                stream=False
            )
            
            # Extract response
            response = chat_completion.choices[0].message.content
            return response
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Error: {str(e)}"

class JarvisBrain:
    def __init__(self):
        self.groq = GroqHandler()
        self.builtin = BuiltinResponses()
        self.classifier = IntentClassifier()
        self.conversation_history = []
    
    def process_query(self, user_input):
        """Main query processing method"""
        try:
            # Clean and validate input
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
            return f"I encountered an error processing your request: {str(e)}"
    
    def _format_response(self, response):
        """Format response for better display"""
        if not response:
            return "I apologize, but I couldn't generate a proper response."
        
        # Clean up response
        response = response.strip()
        
        # Ensure response has proper ending
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
        st.subheader("📡 Status")
        try:
            api_key = st.secrets["GROQ_API_KEY"]
            if api_key and len(api_key) > 10:
                st.success("✅ Groq API Connected")
            else:
                st.error("❌ API Key Not Found")
        except:
            st.error("❌ API Key Not Configured")
            st.info("Add GROQ_API_KEY to your Streamlit secrets")
        
        # Message count
        st.info(f"💬 Messages: {len(st.session_state.messages)}")
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.jarvis.conversation_history = []
            st.rerun()
        
        # Quick commands
        st.subheader("⚡ Quick Commands")
        if st.button("👋 Say Hello"):
            st.session_state.quick_query = "Hello JARVIS"
            
        if st.button("⏰ What time is it?"):
            st.session_state.quick_query = "What time is it?"
            
        if st.button("🤖 Tell me about AI"):
            st.session_state.quick_query = "What is artificial intelligence?"
    
    # Main chat interface
    st.subheader("💬 Chat with JARVIS")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle quick queries from sidebar
    if hasattr(st.session_state, 'quick_query'):
        prompt = st.session_state.quick_query
        del st.session_state.quick_query
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get JARVIS response
        with st.chat_message("assistant"):
            with st.spinner("JARVIS is thinking..."):
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
            with st.spinner("JARVIS is thinking..."):
                response = st.session_state.jarvis.process_query(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
