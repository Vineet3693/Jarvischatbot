
"""
UI Components - Iron Man Themed Interface Elements
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import datetime
from typing import Dict, Any, List
from config import JarvisConfig

class IronManUI:
    """Iron Man themed UI components"""
    
    def __init__(self):
        self.colors = JarvisConfig.COLORS
        self.gradients = JarvisConfig.GRADIENTS
        
    def render_arc_reactor(self, status: str = "online") -> None:
        """Render animated arc reactor"""
        # Create arc reactor visualization
        fig = go.Figure()
        
        # Create concentric circles for arc reactor effect
        theta = np.linspace(0, 2*np.pi, 100)
        
        # Outer ring
        outer_x = 3 * np.cos(theta)
        outer_y = 3 * np.sin(theta)
        
        # Middle ring
        middle_x = 2 * np.cos(theta)
        middle_y = 2 * np.sin(theta)
        
        # Inner ring
        inner_x = 1 * np.cos(theta)
        inner_y = 1 * np.sin(theta)
        
        # Core
        core_x = 0.3 * np.cos(theta)
        core_y = 0.3 * np.sin(theta)
        
        # Add rings with glow effect
        color = self.colors['arc_reactor'] if status == "online" else self.colors['error']
        
        fig.add_trace(go.Scatter(
            x=outer_x, y=outer_y,
            mode='lines',
            line=dict(color=color, width=4),
            fill='tonexty' if len(fig.data) > 0 else None,
            fillcolor=f'rgba(135, 206, 235, 0.1)',
            name='Outer Ring'
        ))
        
        fig.add_trace(go.Scatter(
            x=middle_x, y=middle_y,
            mode='lines',
            line=dict(color=color, width=6),
            fill='tonexty',
            fillcolor=f'rgba(135, 206, 235, 0.2)',
            name='Middle Ring'
        ))
        
        fig.add_trace(go.Scatter(
            x=inner_x, y=inner_y,
            mode='lines',
            line=dict(color=color, width=8),
            fill='tonexty',
            fillcolor=f'rgba(135, 206, 235, 0.3)',
            name='Inner Ring'
        ))
        
        fig.add_trace(go.Scatter(
            x=core_x, y=core_y,
            mode='lines',
            line=dict(color=color, width=10),
            fill='toself',
            fillcolor=f'rgba(135, 206, 235, 0.8)',
            name='Core'
        ))
        
        # Update layout
        fig.update_layout(
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            width=150,
            height=150
        )
        
        st.plotly_chart(fig, use_container_width=False, config={'displayModeBar': False})
    
    def render_system_stats(self, stats: Dict[str, Any]) -> None:
        """Render system statistics panel"""
        st.markdown("### 📊 System Status")
        
        # Status indicators
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_color = self.colors['success'] if stats.get('status') == 'Online' else self.colors['error']
            st.markdown(f"""
            <div style="
                background: {self.gradients['chat']};
                border: 1px solid {status_color};
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                margin-bottom: 10px;
            ">
                <h4 style="color: {status_color}; margin: 0;">Status</h4>
                <p style="color: {self.colors['text']}; margin: 5px 0;">{stats.get('status', 'Unknown')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: {self.gradients['chat']};
                border: 1px solid {self.colors['primary']};
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                margin-bottom: 10px;
            ">
                <h4 style="color: {self.colors['primary']}; margin: 0;">Uptime</h4>
                <p style="color: {self.colors['text']}; margin: 5px 0;">{stats.get('uptime', '00:00:00')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="
                background: {self.gradients['chat']};
                border: 1px solid {self.colors['accent']};
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                margin-bottom: 10px;
            ">
                <h4 style="color: {self.colors['accent']}; margin: 0;">Queries</h4>
                <p style="color: {self.colors['text']}; margin: 5px 0;">{stats.get('total_queries', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed stats
        st.markdown("#### 🔧 Detailed Metrics")
        
        metrics_data = {
            'Conversation Length': stats.get('conversation_length', 0),
            'Last Interaction': stats.get('last_interaction', 'Never'),
            'Memory Usage': f"{stats.get('memory_usage', 0)} bytes",
            'Groq Status': stats.get('groq_status', {}).get('connected', False)
        }
        
        for key, value in metrics_data.items():
            st.metric(key, value)
    
    def render_chat_message(self, role: str, content: str, metadata: Dict = None) -> None:
        """Render enhanced chat message with Iron Man styling"""
        if role == "user":
            # User message
            st.markdown(f"""
            <div style="
                background: linear-gradient(45deg, rgba(255,107,53,0.2), rgba(255,107,53,0.1));
                border-left: 4px solid {self.colors['secondary']};
                border-radius: 0 15px 15px 15px;
                padding: 15px;
                margin: 10px 0;
                margin-left: 50px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            ">
                <p style="color: {self.colors['text']}; margin: 0; font-family: 'Courier New', monospace;">
                    <strong>👤 USER:</strong> {content}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            # JARVIS response
            response_color = self.colors['primary']
            processing_info = ""
            
            if metadata:
                source = metadata.get('source', 'unknown')
                processing_time = metadata.get('processing_time', 0)
                processing_info = f"<small style='opacity: 0.7;'>[{source.upper()} • {processing_time:.2f}s]</small>"
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(45deg, rgba(0,255,255,0.2), rgba(0,255,255,0.1));
                border-left: 4px solid {response_color};
                border-radius: 15px 0 15px 15px;
                padding: 15px;
                margin: 10px 0;
                margin-right: 50px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                position: relative;
            ">
                <p style="color: {response_color}; margin: 0 0 5px 0; font-family: 'Courier New', monospace;">
                    <strong>🤖 JARVIS:</strong> {processing_info}
                </p>
                <p style="color: {self.colors['text']}; margin: 0; line-height: 1.6;">
                    {content}
                </p>
                <div style="
                    position: absolute;
                    top: -5px;
                    left: -5px;
                    width: 10px;
                    height: 10px;
                    background: {response_color};
                    border-radius: 50%;
                    box-shadow: 0 0 10px {response_color};
                    animation: pulse 2s infinite;
                "></div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_quick_commands(self) -> str:
        """Render quick command buttons"""
        st.markdown("### ⚡ Quick Commands")
        
        # Command buttons in grid
        col1, col2 = st.columns(2)
        
        quick_query = None
        
        with col1:
            if st.button("👋 Greet JARVIS", use_container_width=True):
                quick_query = "Hello JARVIS, how are you today?"
            
            if st.button("🧠 Explain AI", use_container_width=True):
                quick_query = "What is artificial intelligence and how does it work?"
            
            if st.button("🚀 Future Tech", use_container_width=True):
                quick_query = "Tell me about future technology trends"
            
            if st.button("⚡ Arc Reactor", use_container_width=True):
                quick_query = "How does Tony Stark's arc reactor work?"
        
        with col2:
            if st.button("⏰ Current Time", use_container_width=True):
                quick_query = "What time is it?"
            
            if st.button("🔬 Science Help", use_container_width=True):
                quick_query = "Explain quantum computing in simple terms"
            
            if st.button("💡 Problem Solving", use_container_width=True):
                quick_query = "Help me think through a complex problem"
            
            if st.button("🎯 System Status", use_container_width=True):
                quick_query = "What is your current system status?"
        
        return quick_query
    
    def render_loading_animation(self) -> None:
        """Render JARVIS thinking animation"""
        st.markdown("""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        ">
            <div style="
                width: 60px;
                height: 60px;
                border: 3px solid rgba(0,255,255,0.2);
                border-top: 3px solid #00ffff;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            "></div>
            <p style="
                color: #00ffff;
                margin-left: 15px;
                font-family: 'Courier New', monospace;
                animation: pulse 1.5s infinite;
            ">JARVIS is processing...</p>
        </div>
        
        <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        </style>
        """, unsafe_allow_html=True)

    def apply_custom_css(self) -> None:
        """Apply custom Iron Man themed CSS"""
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
            font-family: 'Rajdhani', sans-serif;
        }
        
        /* Header Styling */
        .main-header {
            background: linear-gradient(90deg, #00ffff, #ff6b35);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Orbitron', monospace;
            font-weight: 900;
            text-align: center;
            font-size: 3rem;
            margin-bottom: 20px;
            text-shadow: 0 0 20px rgba(0,255,255,0.5);
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%);
            border-right: 2px solid #00ffff;
        }
        
        /* Chat Messages */
        .stChatMessage {
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
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
        
        /* Metrics */
        .metric-container {
            background: rgba(26, 26, 26, 0.8);
            border: 1px solid #00ffff;
            border-radius: 10px;
            padding: 15px;
            backdrop-filter: blur(10px);
        }
        
        /* Input Fields */
        .stTextInput > div > div > input {
            background: rgba(26, 26, 26, 0.8);
            color: #00ffff;
            border: 1px solid #00ffff;
            border-radius: 10px;
            font-family: 'Rajdhani', sans-serif;
        }
        
        /* Chat Input */
        .stChatInput > div {
            background: rgba(26, 26, 26, 0.9);
            border: 2px solid #00ffff;
            border-radius: 15px;
        }
        
        /* Animations */
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 5px #00ffff; }
            50% { box-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff; }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        /* Arc Reactor Glow Effect */
        .arc-reactor {
            animation: glow 2s infinite;
        }
        
        /* Status Indicators */
        .status-online {
            color: #00ff41;
            text-shadow: 0 0 10px #00ff41;
        }
        
        .status-offline {
            color: #ff5722;
            text-shadow: 0 0 10px #ff5722;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1a1a1a;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #00ffff, #ff6b35);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(45deg, #ff6b35, #00ffff);
        }
        </style>
        """, unsafe_allow_html=True)
