
"""
JARVIS AI Assistant - Iron Man Style
Single File Implementation for Streamlit Cloud
"""

import streamlit as st
import datetime
import json
import random
import numpy as np
import plotly.graph_objects as go
from groq import Groq

# Configure Streamlit page
st.set_page_config(
    page_title="JARVIS AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration Class
class Config:
    GROQ_API_KEY = "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"
    MODEL = "llama2-70b-4096"
    MAX_TOKENS = 500
    TEMPERATURE = 0.7

# Apply Iron Man Theme CSS
def apply_iron_man_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(90deg, #00ffff, #ff6b35);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        text-align: center;
        font-size: 3.5rem;
        margin-bottom: 30px;
        text-shadow: 0 0 30px rgba(0,255,255,0.5);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%);
        border-right: 2px solid #00ffff;
    }
    
    /* Chat Messages */
    .user-message {
        background: linear-gradient(45deg, rgba(255,107,53,0.2), rgba(255,107,53,0.1));
        border-left: 4px solid #ff6b35;
        border-radius: 0 15px 15px 15px;
        padding: 15px;
        margin: 10px 50px 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .assistant-message {
        background: linear-gradient(45deg, rgba(0,255,255,0.2), rgba(0,255,255,0.1));
        border-left: 4px solid #00ffff;
        border-radius: 15px 0 15px 15px;
        padding: 15px;
        margin: 10px 0 10px 50px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
    }
    
    .assistant-message::before {
        content: '';
        position: absolute;
        top: -5px;
        left: -5px;
        width: 10px;
        height: 10px;
        background: #00ffff;
        border-radius: 50%;
        box-shadow: 0 0 10px #00ffff;
        animation: pulse 2s infinite;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #00ffff, #ff6b35);
        color: white;
        border: none;
        border-radius: 10px;
        font-family: 'Orbitron', monospace;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,255,255,0.4);
        background: linear-gradient(45deg, #ff6b35, #00ffff);
    }
    
    /* Chat Input */
    .stChatInput > div {
        background: rgba(26, 26, 26, 0.9);
        border: 2px solid #00ffff;
        border-radius: 15px;
    }
    
    /* Animations */
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px #00ffff; }
        50% { box-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff; }
    }
    
    /* Status Indicators */
    .status-online { color: #00ff41; text-shadow: 0 0 10px #00ff41; }
    .status-offline { color: #ff5722; text-shadow: 0 0 10px #ff5722; }
    
    /* Metrics */
    .metric-card {
        background: rgba(26, 26, 26, 0.8);
        border: 1px solid #00ffff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #1a1a1a; }
    ::-webkit-scrollbar-thumb { 
        background: linear-gradient(45deg, #00ffff, #ff6b35);
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# Intent Classifier
class IntentClassifier:
    def __init__(self):
        self.intents = {
            'greeting': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
            'time': ['time', 'clock', 'what time'],
            'date': ['date', 'today', 'what day'],
            'status': ['status', 'how are you', 'system status'],
            'thanks': ['thank you', 'thanks', 'good job']
        }
    
    def classify(self, text):
        text_lower = text.lower()
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        return 'complex'

# Groq Handler
class GroqHandler:
    def __init__(self):
        self.client = None
        self.connected = False
        self.setup_client()
    
    def setup_client(self):
        try:
            # Try to get API key from secrets first
            try:
                api_key = st.secrets["GROQ_API_KEY"]
            except:
                api_key = Config.GROQ_API_KEY
            
            self.client = Groq(api_key=api_key)
            
            # Test connection
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model=Config.MODEL,
                max_tokens=5
            )
            self.connected = True
            
        except Exception as e:
            st.sidebar.error(f"❌ Groq API Error: {str(e)}")
            self.connected = False
    
    def get_response(self, user_input, history=[]):
        if not self.connected:
            return "🔧 I'm not connected to my AI brain. Please check the API configuration."
        
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are JARVIS, Tony Stark's AI assistant from Iron Man.
                    
                    Personality:
                    - Highly intelligent and sophisticated
                    - Professional yet witty
                    - Slight British accent in tone
                    - Confident and capable
                    - Technical expertise
                    
                    Keep responses:
                    - Clear and informative
                    - Under 250 words
                    - Helpful and engaging
                    - Professional but conversational"""
                }
            ]
            
            # Add recent history
            for conv in history[-3:]:
                messages.append({"role": "user", "content": conv.get('user', '')})
                messages.append({"role": "assistant", "content": conv.get('assistant', '')})
            
            messages.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                messages=messages,
                model=Config.MODEL,
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I'm experiencing technical difficulties: {str(e)}"

# Built-in Responses
class BuiltinResponses:
    def __init__(self):
        self.responses = {
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
            ]
        }
    
    def get_response(self, intent, user_input):
        if intent == 'time':
            now = datetime.datetime.now()
            return f"The current time is {now.strftime('%I:%M %p')}, sir."
        elif intent == 'date':
            now = datetime.datetime.now()
            return f"Today is {now.strftime('%A, %B %d, %Y')}."
        elif intent in self.responses:
            return random.choice(self.responses[intent])
        return ""

# Main JARVIS Brain
class JarvisBrain:
    def __init__(self):
        self.groq = GroqHandler()
        self.builtin = BuiltinResponses()
        self.classifier = IntentClassifier()
        self.history = []
    
    def process(self, user_input):
        try:
            intent = self.classifier.classify(user_input)
            
            if intent != 'complex':
                response = self.builtin.get_response(intent, user_input)
                source = 'builtin'
            else:
                response = self.groq.get_response(user_input, self.history)
                source = 'groq'
            
            # Add to history
            self.history.append({
                'user': user_input,
                'assistant': response,
                'intent': intent,
                'source': source,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            # Keep last 10 interactions
            if len(self.history) > 10:
                self.history = self.history[-10:]
            
            return response, {'intent': intent, 'source': source}
            
        except Exception as e:
            return f"I encountered an error: {str(e)}", {'error': True}

# UI Components
def render_arc_reactor(status="online"):
    """Render arc reactor visualization"""
    fig = go.Figure()
    
    # Create concentric circles
    theta = np.linspace(0, 2*np.pi, 100)
    
    rings = [
        (3, '#87ceeb', 2),
        (2, '#00ffff', 4),
        (1, '#87ceeb', 6),
        (0.3, '#ffffff', 8)
    ]
    
    for radius, color, width in rings:
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            line=dict(color=color, width=width),
            fill='toself' if radius == 0.3 else None,
            fillcolor=f'rgba(135, 206, 235, 0.6)' if radius == 0.3 else None,
            showlegend=False
        ))
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, range=[-4, 4]),
        yaxis=dict(visible=False, range=[-4, 4]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        width=120,
        height=120
    )
    
    return fig

def render_chat_message(role, content, metadata=None):
    """Render enhanced chat messages"""
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
            <strong style="color: #ff6b35;">👤 USER:</strong><br>
            <span style="color: white; line-height: 1.6;">{content}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        processing_info = ""
        if metadata:
            source = metadata.get('source', 'unknown')
            processing_info = f"<small style='opacity: 0.7;'>[{source.upper()}]</small>"
        
        st.markdown(f"""
        <div class="assistant-message">
            <strong style="color: #00ffff;">🤖 JARVIS:</strong> {processing_info}<br>
            <span style="color: white; line-height: 1.6;">{content}</span>
        </div>
        """, unsafe_allow_html=True)

def render_system_stats(jarvis):
    """Render system statistics"""
    st.markdown("### 📊 System Status")
    
    # Connection status
    status = "Online" if jarvis.groq.connected else "Offline"
    status_color = "#00ff41" if jarvis.groq.connected else "#ff5722"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {status_color}; margin: 0;">Status</h4>
            <p style="color: white; margin: 5px 0;">{status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        uptime = datetime.datetime.now() - st.session_state.get('start_time', datetime.datetime.now())
        uptime_str = str(uptime).split('.')[0]
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #00ffff; margin: 0;">Uptime</h4>
            <p style="color: white; margin: 5px 0;">{uptime_str}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        query_count = len(st.session_state.get('messages', []))
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #ffd700; margin: 0;">Queries</h4>
            <p style="color: white; margin: 5px 0;">{query_count}</p>
        </div>
        """, unsafe_allow_html=True)

def render_quick_commands():
    """Render quick command buttons"""
    st.markdown("### ⚡ Quick Commands")
    
    col1, col2 = st.columns(2)
    quick_query = None
    
    with col1:
        if st.button("👋 Greet", use_container_width=True):
            quick_query = "Hello JARVIS, how are you?"
        
        if st.button("🧠 AI Info", use_container_width=True):
            quick_query = "What is artificial intelligence?"
        
        if st.button("⚡ Arc Reactor", use_container_width=True):
            quick_query = "How does Tony Stark's arc reactor work?"
    
    with col2:
        if st.button("⏰ Time", use_container_width=True):
            quick_query = "What time is it?"
        
        if st.button("🔬 Science", use_container_width=True):
            quick_query = "Explain quantum computing simply"
        
        if st.button("🎯 Status", use_container_width=True):
            quick_query = "What is your current status?"
    
    return quick_query

def render_neural_activity(activity_level=0.5):
    """Render neural network visualization"""
    fig = go.Figure()
    
    # Create nodes
    layers = [
        (0, 4, '#00ffff'),    # Input layer
        (2, 6, '#ff6b35'),    # Hidden layer
        (4, 3, '#ffd700')     # Output layer
    ]
    
    all_nodes = []
    
    # Add connections and collect nodes
    for i, (x, nodes, color) in enumerate(layers):
        for j in range(nodes):
            y = j - nodes/2 + 0.5
            all_nodes.append((x, y, color))
            
            # Connect to next layer
            if i < len(layers) - 1:
                next_x, next_nodes, _ = layers[i + 1]
                for k in range(next_nodes):
                    next_y = k - next_nodes/2 + 0.5
                    fig.add_trace(go.Scatter(
                        x=[x, next_x], y=[y, next_y],
                        mode='lines',
                        line=dict(color='rgba(255,255,255,0.1)', width=1),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
    
    # Add nodes
    for x, y, color in all_nodes:
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers',
            marker=dict(
                size=15 + 5 * activity_level,
                color=color,
                opacity=0.7 + 0.3 * activity_level,
                line=dict(width=2, color='white')
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=200
    )
    
    return fig

def render_welcome_screen():
    """Render welcome screen for new users"""
    st.markdown("""
    <div style="
        text-align: center;
        padding: 40px;
        background: linear-gradient(45deg, rgba(0,255,255,0.1), rgba(255,107,53,0.1));
        border-radius: 20px;
        margin: 20px 0;
        border: 1px solid rgba(0,255,255,0.3);
        backdrop-filter: blur(10px);
    ">
        <h2 style="color: #00ffff; font-family: 'Orbitron', monospace; margin-bottom: 20px;">
            🤖 Welcome to JARVIS
        </h2>
        <p style="color: white; font-size: 1.2rem; margin: 20px 0; line-height: 1.6;">
            Your advanced AI assistant is <span style="color: #00ff41;">online</span> and ready to help.
        </p>
        <div style="
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 30px 0;
            flex-wrap: wrap;
        ">
            <div style="color: #00ffff; font-size: 1.1rem;">
                🧠 <strong>Intelligent Responses</strong>
            </div>
            <div style="color: #ff6b35; font-size: 1.1rem;">
                ⚡ <strong>Lightning Fast</strong>
            </div>
            <div style="color: #ffd700; font-size: 1.1rem;">
                🎯 <strong>Always Available</strong>
            </div>
        </div>
        <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-top: 20px;">
            Try asking about technology, science, problem-solving, or just have a conversation!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample question buttons
    st.markdown("#### 💡 Try these sample questions:")
    
    col1, col2, col3 = st.columns(3)
    
    sample_query = None
    
    with col1:
        if st.button("🤖 What is AI?", use_container_width=True, key="sample1"):
            sample_query = "What is artificial intelligence and how does it work?"
    
    with col2:
        if st.button("🚀 Future Tech", use_container_width=True, key="sample2"):
            sample_query = "What are the most exciting future technology trends?"
    
    with col3:
        if st.button("⚡ Arc Reactor", use_container_width=True, key="sample3"):
            sample_query = "How does Tony Stark's arc reactor work?"
    
    return sample_query

def render_matrix_background():
    """Render Matrix-style background effect"""
    st.markdown("""
    <div id="matrix-bg" style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        opacity: 0.1;
        overflow: hidden;
    ">
        <canvas id="matrix-canvas" width="100%" height="100%"></canvas>
    </div>
    
    <script>
    if (typeof matrixInitialized === 'undefined') {
        const canvas = document.getElementById('matrix-canvas');
        if (canvas) {
            const ctx = canvas.getContext('2d');
            
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            
            const matrix = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%^&*()";
            const matrixArray = matrix.split("");
            const fontSize = 14;
            const columns = canvas.width / fontSize;
            const drops = [];
            
            for(let x = 0; x < columns; x++) {
                drops[x] = Math.random() * canvas.height;
            }
            
            function draw() {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = '#00ffff';
                ctx.font = fontSize + 'px monospace';
                
                for(let i = 0; i < drops.length; i++) {
                    const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
                    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                    
                    if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                        drops[i] = 0;
                    }
                    drops[i]++;
                }
            }
            
            setInterval(draw, 50);
            window.matrixInitialized = true;
            
            window.addEventListener('resize', function() {
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            });
        }
    }
    </script>
    """, unsafe_allow_html=True)

# Main Application
def main():
    # Apply theme
    apply_iron_man_theme()
    
    # Render background effect
    render_matrix_background()
    
    # Initialize session state
    if 'jarvis_brain' not in st.session_state:
        st.session_state.jarvis_brain = JarvisBrain()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'start_time' not in st.session_state:
        st.session_state.start_time = datetime.datetime.now()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        🤖 JARVIS
        <div style="
            font-size: 1.2rem;
            color: rgba(0,255,255,0.8);
            font-weight: 400;
            margin-top: 10px;
        ">
            Just A Rather Very Intelligent System
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create main layout
    main_col, sidebar_col = st.columns([3, 1])
    
    with main_col:
        # Welcome screen or chat history
        if not st.session_state.messages:
            sample_query = render_welcome_screen()
            if sample_query:
                st.session_state.sample_query = sample_query
                st.rerun()
        
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                render_chat_message("user", message["content"])
            else:
                metadata = message.get("metadata", {})
                render_chat_message("assistant", message["content"], metadata)
        
        # Chat input
        if prompt := st.chat_input("Communicate with JARVIS..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            render_chat_message("user", prompt)
            
            # Get AI response
            with st.spinner("🤖 JARVIS is processing..."):
                response, metadata = st.session_state.jarvis_brain.process(prompt)
            
            # Add assistant response
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "metadata": metadata
            })
            render_chat_message("assistant", response, metadata)
            
            st.rerun()
        
        # Handle sample query
        if hasattr(st.session_state, 'sample_query'):
            prompt = st.session_state.sample_query
            del st.session_state.sample_query
            
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            render_chat_message("user", prompt)
            
            # Get AI response
            with st.spinner("🤖 JARVIS is processing..."):
                response, metadata = st.session_state.jarvis_brain.process(prompt)
            
            # Add assistant response
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "metadata": metadata
            })
            render_chat_message("assistant", response, metadata)
            
            st.rerun()
    
    with sidebar_col:
        # Arc Reactor and Status
        st.markdown("### ⚡ Arc Reactor Core")
        
        reactor_col, status_col = st.columns([1, 2])
        
        with reactor_col:
            reactor_fig = render_arc_reactor()
            st.plotly_chart(reactor_fig, use_container_width=True, config={'displayModeBar': False})
        
        with status_col:
            if st.session_state.jarvis_brain.groq.connected:
                st.markdown('<p class="status-online">🟢 ONLINE</p>', unsafe_allow_html=True)
                st.markdown("**AI Brain:** Active")
                st.markdown("**Model:** Llama 2 70B")
            else:
                st.markdown('<p class="status-offline">🔴 OFFLINE</p>', unsafe_allow_html=True)
                st.markdown("**Status:** Disconnected")
        
        st.markdown("---")
        
        # System Stats
        render_system_stats(st.session_state.jarvis_brain)
        
        st.markdown("---")
        
        # Quick Commands
        quick_query = render_quick_commands()
        if quick_query:
            st.session_state.sample_query = quick_query
            st.rerun()
        
        st.markdown("---")
        
        # Neural Activity
        st.markdown("### 🧠 Neural Activity")
        activity_level = min(1.0, len(st.session_state.messages) / 10)
        neural_fig = render_neural_activity(activity_level)
        st.plotly_chart(neural_fig, use_container_width=True, config={'displayModeBar': False})
        
        # System Controls
        st.markdown("---")
        st.markdown("### 🛠️ System Controls")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.jarvis_brain.history = []
            st.success("✅ Chat cleared!")
            st.rerun()
        
        # Export conversation
        if st.button("💾 Export Chat", use_container_width=True):
            if st.session_state.messages:
                export_data = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "total_messages": len(st.session_state.messages),
                    "conversation": st.session_state.messages,
                    "jarvis_version": "1.0.0"
                }
                
                export_json = json.dumps(export_data, indent=2, ensure_ascii=False)
                
                st.download_button(
                    label="📥 Download JSON",
                    data=export_json,
                    file_name=f"jarvis_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ No conversation to export!")
        
        # Advanced Settings
        with st.expander("⚙️ Advanced Settings"):
            # Temperature slider
            current_temp = st.slider(
                "🌡️ AI Temperature", 
                min_value=0.1, 
                max_value=1.0, 
                value=Config.TEMPERATURE, 
                step=0.1,
                help="Higher values make responses more creative"
            )
            if current_temp != Config.TEMPERATURE:
                Config.TEMPERATURE = current_temp
                st.success(f"Temperature updated to {current_temp}")
            
            # Max tokens
            current_tokens = st.number_input(
                "📝 Max Response Tokens",
                min_value=100,
                max_value=1000,
                value=Config.MAX_TOKENS,
                step=50,
                help="Maximum length of AI responses"
            )
            if current_tokens != Config.MAX_TOKENS:
                Config.MAX_TOKENS = current_tokens
            
            # Reconnect button
            if st.button("🔄 Reconnect to Groq", use_container_width=True):
                st.session_state.jarvis_brain.groq.setup_client()
                st.rerun()
        
        # Debug Information
        with st.expander("🔧 Debug Information"):
            st.write("**Session Information:**")
            st.write(f"- Messages: {len(st.session_state.messages)}")
            st.write(f"- History: {len(st.session_state.jarvis_brain.history)}")
            st.write(f"- Start Time: {st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"- Groq Connected: {st.session_state.jarvis_brain.groq.connected}")
            
            if st.session_state.jarvis_brain.history:
                st.write("**Recent Intents:**")
                recent_intents = [h.get('intent', 'unknown') for h in st.session_state.jarvis_brain.history[-5:]]
                for i, intent in enumerate(recent_intents, 1):
                    st.write(f"  {i}. {intent}")
        
        # Performance Metrics
        st.markdown("---")
        st.markdown("### 📈 Performance")
        
        # Calculate session metrics
        session_duration = datetime.datetime.now() - st.session_state.start_time
        total_messages = len(st.session_state.messages)
        
        # Display metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="💬 Total Messages",
                value=total_messages,
                delta=f"+{total_messages - len(st.session_state.jarvis_brain.history)}"
            )
        
        with col2:
            messages_per_minute = (total_messages / max(session_duration.total_seconds() / 60, 1))
            st.metric(
                label="📊 Msg/Min",
                value=f"{messages_per_minute:.1f}",
                delta="Active Session"
            )
        
        # System Health Bar
        st.markdown("**System Health:**")
        
        # Calculate health score
        health_score = 0.0
        
        if st.session_state.jarvis_brain.groq.connected:
            health_score += 0.6  # 60% for API connection
        
        if len(st.session_state.messages) > 0:
            health_score += 0.2  # 20% for active usage
        
        if session_duration.total_seconds() > 60:
            health_score += 0.2  # 20% for session stability
        
        # Display health bar
        health_percentage = int(health_score * 100)
        health_color = "#00ff41" if health_percentage > 80 else "#ff9800" if health_percentage > 50 else "#ff5722"
        
        st.markdown(f"""
        <div style="
            background: rgba(26,26,26,0.8);
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
        ">
            <div style="
                background: {health_color};
                height: 20px;
                width: {health_percentage}%;
                border-radius: 5px;
                transition: width 0.3s ease;
            "></div>
            <p style="text-align: center; margin: 5px 0; color: {health_color};">
                {health_percentage}% Operational
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="
        text-align: center;
        color: rgba(255,255,255,0.6);
        font-family: 'Rajdhani', sans-serif;
        padding: 20px 0;
        margin-top: 30px;
    ">
        <p style="margin: 5px 0;">
            🤖 <strong>JARVIS AI Assistant</strong> v1.0 | Powered by 
            <span style="color: #00ffff;">Groq Lightning Inference</span>
        </p>
        <p style="margin: 5px 0;">
            Built with ❤️ using <span style="color: #ff6b35;">Streamlit</span> | 
            Iron Man Inspired Design
        </p>
        <div style="
            width: 100px;
            height: 1px;
            background: linear-gradient(90deg, #00ffff, #ff6b35);
            margin: 15px auto;
        "></div>
        <p style="margin: 5px 0; font-size: 0.9rem; opacity: 0.7;">
            "Sometimes you gotta run before you can walk" - Tony Stark
        </p>
    </div>
    """, unsafe_allow_html=True)

# Application Entry Point
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("🚨 **System Error Detected**")
        st.error(f"Error Details: {str(e)}")
        
        with st.expander("🔧 Technical Details"):
            import traceback
            st.code(traceback.format_exc())
        
        st.markdown("""
        ### 🔄 Troubleshooting Steps:
        1. **Refresh the page** - Try reloading the application
        2. **Check API Key** - Ensure your Groq API key is valid
        3. **Clear Browser Cache** - Clear cache and cookies
        4. **Contact Support** - If the issue persists
        """)
        
        # Emergency restart button
        if st.button("🆘 Emergency Restart", type="primary"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
