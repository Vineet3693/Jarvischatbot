
"""
JARVIS AI Assistant - Main Application
Iron Man Themed AI Assistant powered by Groq
"""

import streamlit as st
import sys
import os
import datetime
from typing import Dict, Any

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

# Import JARVIS modules
try:
    from jarvis_core import JarvisCore
    from ui_components import IronManUI
    from animations import JarvisAnimations
    from utils import validate_input, generate_conversation_summary
    from config import JarvisConfig
except ImportError as e:
    st.error(f"Failed to import JARVIS modules: {str(e)}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title=JarvisConfig.APP_TITLE,
    page_icon=JarvisConfig.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/jarvis-assistant',
        'Report a bug': 'https://github.com/your-repo/jarvis-assistant/issues',
        'About': "JARVIS AI Assistant - Iron Man Style"
    }
)

class JarvisApp:
    """Main JARVIS Application Class"""
    
    def __init__(self):
        self.ui = IronManUI()
        self.animations = JarvisAnimations()
        self.initialize_session_state()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'jarvis_core' not in st.session_state:
            st.session_state.jarvis_core = JarvisCore()
        
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'session_start' not in st.session_state:
            st.session_state.session_start = datetime.datetime.now()
        
        if 'total_queries' not in st.session_state:
            st.session_state.total_queries = 0
        
        if 'last_interaction' not in st.session_state:
            st.session_state.last_interaction = None
    
    def render_header(self):
        """Render main header with JARVIS branding"""
        st.markdown("""
        <div class="main-header" style="text-align: center; margin-bottom: 30px;">
            <h1 style="
                background: linear-gradient(90deg, #00ffff, #ff6b35);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-family: 'Orbitron', monospace;
                font-size: 3.5rem;
                margin: 0;
                text-shadow: 0 0 30px rgba(0,255,255,0.5);
            ">
                🤖 JARVIS
            </h1>
            <p style="
                color: #00ffff;
                font-family: 'Rajdhani', sans-serif;
                font-size: 1.2rem;
                margin: 10px 0;
                opacity: 0.8;
            ">
                Just A Rather Very Intelligent System
            </p>
            <div style="
                width: 100px;
                height: 2px;
                background: linear-gradient(90deg, #00ffff, #ff6b35);
                margin: 20px auto;
                border-radius: 1px;
            "></div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render enhanced sidebar with system controls"""
        with st.sidebar:
            # Arc Reactor Status
            st.markdown("### ⚡ Arc Reactor")
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Mini arc reactor visualization
                if st.session_state.jarvis_core.system_status['online']:
                    self.ui.render_arc_reactor("online")
                else:
                    self.ui.render_arc_reactor("offline")
            
            with col2:
                # System status
                stats = st.session_state.jarvis_core.get_system_stats()
                status_color = "🟢" if stats['status'] == 'Online' else "🔴"
                st.markdown(f"**Status:** {status_color} {stats['status']}")
                st.markdown(f"**Uptime:** {stats['uptime']}")
                st.markdown(f"**Queries:** {stats['total_queries']}")
            
            st.markdown("---")
            
            # Quick Commands
            quick_query = self.ui.render_quick_commands()
            if quick_query:
                st.session_state.quick_query = quick_query
            
            st.markdown("---")
            
            # System Controls
            st.markdown("### 🛠️ System Controls")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Clear Chat", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state.jarvis_core.clear_conversation()
                    st.success("Chat cleared!")
                    st.rerun()
            
            with col2:
                if st.button("📊 Stats", use_container_width=True):
                    st.session_state.show_stats = True
            
            # Export conversation
            if st.button("💾 Export Chat", use_container_width=True):
                if st.session_state.messages:
                    export_data = st.session_state.jarvis_core.export_conversation()
                    st.download_button(
                        label="📥 Download JSON",
                        data=export_data,
                        file_name=f"jarvis_conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                else:
                    st.warning("No conversation to export!")
            
            st.markdown("---")
            
            # Advanced Settings
            with st.expander("⚙️ Advanced Settings"):
                # Temperature control
                new_temp = st.slider("AI Temperature", 0.1, 1.0, 0.7, 0.1)
                if new_temp != JarvisConfig.TEMPERATURE:
                    JarvisConfig.TEMPERATURE = new_temp
                    st.success(f"Temperature set to {new_temp}")
                
                # Max tokens
                new_tokens = st.number_input("Max Response Tokens", 100, 1000, 500, 50)
                if new_tokens != JarvisConfig.MAX_TOKENS:
                    JarvisConfig.MAX_TOKENS = new_tokens
                
                # Enable animations
                animations_enabled = st.checkbox("Enable Animations", value=True)
                JarvisConfig.ENABLE_ANIMATIONS = animations_enabled
            
            # System Statistics
            if hasattr(st.session_state, 'show_stats') and st.session_state.show_stats:
                st.markdown("---")
                self.render_detailed_stats()
    
    def render_detailed_stats(self):
        """Render detailed system statistics"""
        st.markdown("### 📈 Detailed Statistics")
        
        # Get conversation summary
        summary = generate_conversation_summary(st.session_state.jarvis_core.conversation_history)
        
        # Display metrics
        st.metric("Total Messages", summary.get('total_messages', 0))
        st.metric("Session Duration", summary.get('session_duration', '00:00:00'))
        st.metric("Avg Processing Time", f"{summary.get('avg_processing_time', 0):.3f}s")
        
        # Intent distribution
        if summary.get('intent_distribution'):
            st.markdown("**Intent Distribution:**")
            for intent, count in summary['intent_distribution'].items():
                st.write(f"• {intent.title()}: {count}")
        
        # Close stats
        if st.button("❌ Close Stats"):
            del st.session_state.show_stats
            st.rerun()
    
    def render_main_chat(self):
        """Render main chat interface"""
        # Chat header
        st.markdown("### 💬 Communication Interface")
        
        # Display conversation messages
        chat_container = st.container()
        
        with chat_container:
            for i, message in enumerate(st.session_state.messages):
                # Get metadata if available
                metadata = None
                if i < len(st.session_state.jarvis_core.conversation_history):
                    metadata = st.session_state.jarvis_core.conversation_history[i]
                
                self.ui.render_chat_message(
                    role=message["role"],
                    content=message["content"],
                    metadata=metadata
                )
        
        # Handle quick queries
        if hasattr(st.session_state, 'quick_query'):
            self.process_user_input(st.session_state.quick_query)
            del st.session_state.quick_query
            st.rerun()
        
        # Chat input
        if prompt := st.chat_input("Communicate with JARVIS..."):
            self.process_user_input(prompt)
    
    def process_user_input(self, user_input: str):
        """Process user input and generate response"""
        # Validate input
        is_valid, error_message = validate_input(user_input)
        if not is_valid:
            st.error(f"Input validation failed: {error_message}")
            return
        
        # Update counters
        st.session_state.total_queries += 1
        st.session_state.last_interaction = datetime.datetime.now()
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message immediately
        self.ui.render_chat_message("user", user_input)
        
        # Show processing animation
        with st.spinner("JARVIS is processing your request..."):
            # Get response from JARVIS core
            response, metadata = st.session_state.jarvis_core.process_query(user_input)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant response
        self.ui.render_chat_message("assistant", response, metadata)
    
    def render_system_monitor(self):
        """Render system monitoring panel"""
        if JarvisConfig.ENABLE_ANIMATIONS:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Neural network visualization
                st.markdown("#### 🧠 Neural Activity")
                activity_level = min(1.0, len(st.session_state.messages) / 10.0)
                neural_viz = self.animations.create_neural_network_viz(activity_level)
                st.plotly_chart(neural_viz, use_container_width=True, config={'displayModeBar': False})
            
            with col2:
                # System metrics
                st.markdown("#### 📊 System Metrics")
                
                # Simulated system stats
                import random
                cpu_usage = random.randint(20, 80)
                memory_usage = random.randint(30, 70)
                network_activity = random.randint(10, 90)
                
                st.progress(cpu_usage / 100, text=f"CPU: {cpu_usage}%")
                st.progress(memory_usage / 100, text=f"Memory: {memory_usage}%")
                st.progress(network_activity / 100, text=f"Network: {network_activity}%")
    
    def render_welcome_screen(self):
        """Render welcome screen for new users"""
        if not st.session_state.messages:
            st.markdown("""
            <div style="
                text-align: center;
                padding: 40px;
                background: linear-gradient(45deg, rgba(0,255,255,0.1), rgba(255,107,53,0.1));
                border-radius: 20px;
                margin: 20px 0;
                border: 1px solid rgba(0,255,255,0.3);
            ">
                <h2 style="color: #00ffff; font-family: 'Orbitron', monospace;">
                    Welcome to JARVIS
                </h2>
                <p style="color: white; font-size: 1.1rem; margin: 20px 0;">
                    Your advanced AI assistant is online and ready to help.
                </p>
                <div style="
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    margin: 30px 0;
                ">
                    <div style="color: #00ffff;">🧠 Intelligent Responses</div>
                    <div style="color: #ff6b35;">⚡ Lightning Fast</div>
                    <div style="color: #ffd700;">🎯 Always Available</div>
                </div>
                <p style="color: rgba(255,255,255,0.7);">
                    Try asking me about technology, science, problem-solving, or just have a conversation!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Sample questions
            st.markdown("#### 💡 Try these sample questions:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🤖 What is AI?", use_container_width=True):
                    st.session_state.quick_query = "What is artificial intelligence and how does it work?"
            
            with col2:
                if st.button("🚀 Future Tech", use_container_width=True):
                    st.session_state.quick_query = "What are the most exciting future technology trends?"
            
            with col3:
                if st.button("⚡ Arc Reactor", use_container_width=True):
                    st.session_state.quick_query = "How does Tony Stark's arc reactor work?"
    
    def run(self):
        """Main application runner"""
        # Apply custom styling
        self.ui.apply_custom_css()
        
        # Render matrix background effect (if animations enabled)
        if JarvisConfig.ENABLE_ANIMATIONS:
            self.animations.render_matrix_rain()
        
        # Main layout
        self.render_header()
        
        # Create main columns
        main_col, monitor_col = st.columns([3, 1])
        
        with main_col:
            # Welcome screen or chat
            if not st.session_state.messages:
                self.render_welcome_screen()
            
            # Main chat interface
            self.render_main_chat()
        
        with monitor_col:
            # System monitoring
            self.render_system_monitor()
        
        # Render sidebar
        self.render_sidebar()
        
        # Footer
        self.render_footer()
    
    def render_footer(self):
        """Render application footer"""
        st.markdown("---")
        st.markdown("""
        <div style="
            text-align: center;
            color: rgba(255,255,255,0.5);
            font-family: 'Rajdhani', sans-serif;
            padding: 20px 0;
        ">
            <p>🤖 JARVIS AI Assistant v1.0 | Powered by Groq Lightning Inference</p>
            <p>Built with ❤️ using Streamlit | Iron Man Inspired Design</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    try:
        # Initialize and run JARVIS app
        app = JarvisApp()
        app.run()
        
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.error("Please refresh the page or contact support if the problem persists.")
        
        # Show error details in expander
        with st.expander("🔧 Error Details"):
            st.code(str(e))

if __name__ == "__main__":
    main()
