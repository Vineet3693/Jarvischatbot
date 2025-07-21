
import streamlit as st
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from jarvis_brain import JarvisBrain

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
            quick_query = "Hello JARVIS"
            st.session_state.quick_query = quick_query
            
        if st.button("⏰ What time is it?"):
            quick_query = "What time is it?"
            st.session_state.quick_query = quick_query
    
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



