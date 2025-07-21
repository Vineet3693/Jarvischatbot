
"""
JARVIS AI Assistant - Iron Man Style
Ultra-Compatible Version for Streamlit Cloud
"""

import streamlit as st
import datetime
import json
import random
from groq import Groq

# Page Config
st.set_page_config(
    page_title="🤖 JARVIS AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
GROQ_API_KEY = "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"
MODEL = "llama2-70b-4096"

# Apply Iron Man Theme
def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a, #1a1a1a);
        color: #ffffff;
        font-family: 'Orbitron', monospace;
    }
    
    .main-title {
        background: linear-gradient(90deg, #00ffff, #ff6b35);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 0 0 30px rgba(0,255,255,0.5);
    }
    
    .user-msg {
        background: linear-gradient(45deg, rgba(255,107,53,0.2), rgba(255,107,53,0.1));
        border-left: 4px solid #ff6b35;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: white;
    }
    
    .jarvis-msg {
        background: linear-gradient(45deg, rgba(0,255,255,0.2), rgba(0,255,255,0.1));
        border-left: 4px solid #00ffff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: white;
    }
    
    .status-online {
        color: #00ff41;
        font-weight: bold;
    }
    
    .status-offline {
        color: #ff5722;
        font-weight: bold;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #00ffff, #ff6b35);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,255,255,0.4);
    }
    
    .metric-box {
        background: rgba(26,26,26,0.8);
        border: 1px solid #00ffff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
    }
    
    .sidebar .stSelectbox {
        background: rgba(26,26,26,0.8);
    }
    </style>
    """, unsafe_allow_html=True)

# Intent Classifier
def classify_intent(text):
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return 'greeting'
    elif any(word in text_lower for word in ['time', 'clock']):
        return 'time'
    elif any(word in text_lower for word in ['date', 'today']):
        return 'date'
    elif any(word in text_lower for word in ['status', 'how are you']):
        return 'status'
    elif any(word in text_lower for word in ['thank', 'thanks']):
        return 'thanks'
    else:
        return 'complex'

# Built-in Responses
def get_builtin_response(intent):
    responses = {
        'greeting': [
            "Good day! JARVIS at your service. How may I assist you?",
            "Hello! I'm online and ready to help. What can I do for you?",
            "Greetings! Your AI assistant is active. How can I help?",
            "Welcome back! JARVIS reporting for duty."
        ],
        'status': [
            "All systems operational, sir. Running at optimal performance.",
            "I'm functioning perfectly. Ready to assist.",
            "System status: Green. All modules online and responsive."
        ],
        'thanks': [
            "You're quite welcome. Always happy to assist.",
            "My pleasure, sir. Is there anything else you need?",
            "Glad I could help. I'm here whenever you need me."
        ],
        'time': [f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}, sir."],
        'date': [f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."]
    }
    
    return random.choice(responses.get(intent, ["I understand."]))

# Groq Handler
class GroqHandler:
    def __init__(self):
        self.client = None
        self.connected = False
        self.setup()
    
    def setup(self):
        try:
            # Try secrets first
            try:
                api_key = st.secrets["GROQ_API_KEY"]
            except:
                api_key = GROQ_API_KEY
            
            self.client = Groq(api_key=api_key)
            
            # Test connection
            test_response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model=MODEL,
                max_tokens=5
            )
            self.connected = True
            
        except Exception as e:
            self.connected = False
            st.sidebar.error(f"❌ API Error: {str(e)}")
    
    def get_response(self, prompt, history=[]):
        if not self.connected:
            return "🔧 I'm not connected to my AI brain. Please check the configuration."
        
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are JARVIS, Tony Stark's AI assistant from Iron Man.
                    
                    You are:
                    - Highly intelligent and sophisticated
                    - Professional yet witty
                    - Confident and capable
                    - Have a slight British accent in your tone
                    
                    Keep responses:
                    - Clear and informative
                    - Under 200 words
                    - Helpful and engaging
                    - Professional but conversational"""
                }
            ]
            
            # Add recent history (last 2 exchanges)
            for conv in history[-2:]:
                if 'user' in conv and 'assistant' in conv:
                    messages.append({"role": "user", "content": conv['user']})
                    messages.append({"role": "assistant", "content": conv['assistant']})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                messages=messages,
                model=MODEL,
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I'm experiencing technical difficulties: {str(e)}"

# Main App
def main():
    # Apply theme
    apply_theme()
    
    # Initialize session state
    if 'groq_handler' not in st.session_state:
        st.session_state.groq_handler = GroqHandler()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'start_time' not in st.session_state:
        st.session_state.start_time = datetime.datetime.now()
    
    # Header
    st.markdown('<h1 class="main-title">🤖 JARVIS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #00ffff; font-size: 1.2rem;">Just A Rather Very Intelligent System</p>', unsafe_allow_html=True)
    
    # Create columns
    main_col, sidebar_col = st.columns([3, 1])
    
    with main_col:
        # Welcome message
        if not st.session_state.messages:
            st.markdown("""
            <div style="
                background: linear-gradient(45deg, rgba(0,255,255,0.1), rgba(255,107,53,0.1));
                border: 1px solid rgba(0,255,255,0.3);
                border-radius: 15px;
                padding: 30px;
                text-align: center;
                margin: 20px 0;
            ">
                <h2 style="color: #00ffff; margin-bottom: 15px;">Welcome to JARVIS</h2>
                <p style="color: white; font-size: 1.1rem;">Your advanced AI assistant is online and ready to help.</p>
                <div style="margin: 20px 0;">
                    <span style="color: #00ffff;">🧠 Intelligent</span> •
                    <span style="color: #ff6b35;">⚡ Fast</span> •
                    <span style="color: #ffd700;">🎯 Available</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Sample questions
            st.markdown("#### 💡 Try asking:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🤖 What is AI?", use_container_width=True):
                    st.session_state.sample_query = "What is artificial intelligence?"
            
            with col2:
                if st.button("🚀 Future Tech", use_container_width=True):
                    st.session_state.sample_query = "Tell me about future technology"
            
            with col3:
                if st.button("⚡ Arc Reactor", use_container_width=True):
                    st.session_state.sample_query = "How does an arc reactor work?"
        
        # Display messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-msg"><strong>👤 USER:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
            else:
                metadata = message.get("metadata", {})
                source_info = f"[{metadata.get('source', 'unknown').upper()}]" if metadata else ""
                st.markdown(f'<div class="jarvis-msg"><strong>🤖 JARVIS:</strong> <small>{source_info}</small><br>{message["content"]}</div>', unsafe_allow_html=True)
        
        # Handle sample query
        if hasattr(st.session_state, 'sample_query'):
            prompt = st.session_state.sample_query
            del st.session_state.sample_query
            process_input(prompt)
            st.rerun()
        
        # Chat input
        if prompt := st.chat_input("Communicate with JARVIS..."):
            process_input(prompt)
    
    with sidebar_col:
        # Status
        st.markdown("### ⚡ System Status")
        
        if st.session_state.groq_handler.connected:
            st.markdown('<p class="status-online">🟢 ONLINE</p>', unsafe_allow_html=True)
            st.write("**AI Brain:** Active")
            st.write("**Model:** Llama 2 70B")
        else:
            st.markdown('<p class="status-offline">🔴 OFFLINE</p>', unsafe_allow_html=True)
            st.write("**Status:** Disconnected")
        
        # Metrics
        st.markdown("---")
        st.markdown("### 📊 Metrics")
        
        uptime = datetime.datetime.now() - st.session_state.start_time
        uptime_str = str(uptime).split('.')[0]
        
        st.markdown(f"""
        <div class="metric-box">
            <h4 style="color: #00ffff; margin: 0;">Uptime</h4>
            <p style="margin: 5px 0;">{uptime_str}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-box">
            <h4 style="color: #ff6b35; margin: 0;">Messages</h4>
            <p style="margin: 5px 0;">{len(st.session_state.messages)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick commands
        st.markdown("---")
        st.markdown("### ⚡ Quick Commands")
        
        if st.button("👋 Hello", use_container_width=True):
            st.session_state.sample_query = "Hello JARVIS"
            st.rerun()
        
        if st.button("⏰ Time", use_container_width=True):
            st.session_state.sample_query = "What time is it?"
            st.rerun()
        
        if st.button("🎯 Status", use_container_width=True):
            st.session_state.sample_query = "What is your status?"
            st.rerun()
        
        # Controls
        st.markdown("---")
        st.markdown("### 🛠️ Controls")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.success("✅ Chat cleared!")
            st.rerun()
        
        if st.button("🔄 Reconnect", use_container_width=True):
            st.session_state.groq_handler.setup()
            st.rerun()
        
        # Export
        if st.button("💾 Export", use_container_width=True):
            if st.session_state.messages:
                export_data = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "messages": st.session_state.messages,
                    "total_messages": len(st.session_state.messages)
                }
                
                st.download_button(
                    label="📥 Download JSON",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"jarvis_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("⚠️ No conversation to export!")

def process_input(user_input):
    """Process user input and generate response"""
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Classify intent
    intent = classify_intent(user_input)
    
    # Generate response
    if intent != 'complex':
        # Use built-in response
        response = get_builtin_response(intent)
        source = 'builtin'
    else:
        # Use Groq AI
        with st.spinner("🤖 JARVIS is thinking..."):
            response = st.session_state.groq_handler.get_response(
                user_input, 
                st.session_state.conversation_history
            )
        source = 'groq'
    
    # Add to conversation history
    conversation_entry = {
        'user': user_input,
        'assistant': response,
        'intent': intent,
        'source': source,
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    st.session_state.conversation_history.append(conversation_entry)
    
    # Keep only last 10 conversations
    if len(st.session_state.conversation_history) > 10:
        st.session_state.conversation_history = st.session_state.conversation_history[-10:]
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "metadata": {"intent": intent, "source": source}
    })
    
    st.rerun()

# Footer
def render_footer():
    st.markdown("---")
    st.markdown("""
    <div style="
        text-align: center;
        color: rgba(255,255,255,0.6);
        padding: 20px 0;
        margin-top: 30px;
    ">
        <p>🤖 <strong>JARVIS AI Assistant</strong> v1.0 | Powered by <span style="color: #00ffff;">Groq</span></p>
        <p>Built with ❤️ using <span style="color: #ff6b35;">Streamlit</span> | Iron Man Inspired</p>
        <p style="font-style: italic; opacity: 0.7; margin-top: 10px;">
            "Sometimes you gotta run before you can walk" - Tony Stark
        </p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    try:
        main()
        render_footer()
    except Exception as e:
        st.error("🚨 **System Error**")
        st.error(f"Error: {str(e)}")
        
        st.markdown("""
        ### 🔄 Troubleshooting:
        1. **Refresh the page**
        2. **Check your internet connection** 
        3. **Verify API key is working**
        4. **Try again in a few moments**
        """)
        
        if st.button("🆘 Emergency Restart"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
