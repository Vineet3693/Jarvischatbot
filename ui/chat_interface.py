
import streamlit as st

def render_chat_interface():
    """Render the main chat interface"""
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    return chat_container

def render_sidebar():
    """Render sidebar with controls"""
    
    with st.sidebar:
        st.header("🛠️ JARVIS Controls")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.jarvis.conversation_history = []
            st.rerun()
        
        # Status indicators
        st.header("📊 Status")
        st.success("✅ Groq API Connected")
        st.info(f"💬 Messages: {len(st.session_state.messages)}")
        
        # Quick commands
        st.header("⚡ Quick Commands")
        if st.button("What time is it?"):
            return "What time is it?"
        if st.button("Hello JARVIS"):
            return "Hello JARVIS"
        
    return None
