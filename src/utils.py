
"""
Utility Functions for JARVIS Assistant
"""
import datetime
import json
import os
import re
from typing import Dict, Any, List, Optional
import streamlit as st

def format_response(response: str) -> str:
    """Format AI response for better display"""
    if not response or not response.strip():
        return "I apologize, but I couldn't generate a proper response."
    
    # Clean up response
    response = response.strip()
    
    # Remove excessive whitespace
    response = re.sub(r'\n\s*\n', '\n\n', response)
    response = re.sub(r' +', ' ', response)
    
    # Ensure proper sentence ending
    if not response.endswith(('.', '!', '?', ':')):
        response += '.'
    
    # Capitalize first letter
    if response and response[0].islower():
        response = response[0].upper() + response[1:]
    
    return response

def log_interaction(interaction: Dict[str, Any]) -> None:
    """Log user interactions for analytics and debugging"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Prepare log entry
        log_entry = {
            'timestamp': interaction.get('timestamp', datetime.datetime.now().isoformat()),
            'user_input': interaction.get('user', '')[:100],  # Limit length
            'response': interaction.get('assistant', '')[:200],  # Limit length
            'intent': interaction.get('intent', 'unknown'),
            'source': interaction.get('source', 'unknown'),
            'processing_time': interaction.get('processing_time', 0),
            'session_id': get_session_id()
        }
        
        # Write to log file
        log_file = f"data/interactions_{datetime.datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
            
    except Exception as e:
        # Silently fail logging to not break the app
        st.error(f"Logging error: {str(e)}")

def get_session_id() -> str:
    """Get or create session ID"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return st.session_state.session_id

def validate_input(user_input: str) -> tuple[bool, str]:
    """Validate user input"""
    if not user_input or not user_input.strip():
        return False, "Empty input"
    
    if len(user_input) > 2000:
        return False, "Input too long (max 2000 characters)"
    
    # Check for potential security issues
    dangerous_patterns = ['<script', 'javascript:', 'eval(', 'exec(']
    for pattern in dangerous_patterns:
        if pattern.lower() in user_input.lower():
            return False, "Invalid input detected"
    
    return True, "Valid"

def calculate_response_metrics(start_time: datetime.datetime, end_time: datetime.datetime) -> Dict[str, float]:
    """Calculate response time metrics"""
    duration = end_time - start_time
    return {
        'response_time': duration.total_seconds(),
        'response_time_ms': duration.total_seconds() * 1000
    }

def export_conversation_history(conversation_history: List[Dict]) -> str:
    """Export conversation history as formatted text"""
    export_data = {
        'export_timestamp': datetime.datetime.now().isoformat(),
        'total_interactions': len(conversation_history),
        'conversation': conversation_history
    }
    
    return json.dumps(export_data, indent=2, ensure_ascii=False)

def generate_conversation_summary(conversation_history: List[Dict]) -> Dict[str, Any]:
    """Generate summary statistics for conversation"""
    if not conversation_history:
        return {'total_messages': 0}
    
    total_messages = len(conversation_history)
    intents = [conv.get('intent', 'unknown') for conv in conversation_history]
    sources = [conv.get('source', 'unknown') for conv in conversation_history]
    processing_times = [conv.get('processing_time', 0) for conv in conversation_history]
    
    # Calculate statistics
    intent_counts = {}
    for intent in intents:
        intent_counts[intent] = intent_counts.get(intent, 0) + 1
    
    source_counts = {}
    for source in sources:
        source_counts[source] = source_counts.get(source, 0) + 1
    
    avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
    
    return {
        'total_messages': total_messages,
        'intent_distribution': intent_counts,
        'source_distribution': source_counts,
        'avg_processing_time': round(avg_processing_time, 3),
        'session_duration': get_session_duration(),
        'most_common_intent': max(intent_counts.items(), key=lambda x: x[1])[0] if intent_counts else 'unknown'
    }

def get_session_duration() -> str:
    """Get current session duration"""
    if 'session_start' not in st.session_state:
        st.session_state.session_start = datetime.datetime.now()
    
    duration = datetime.datetime.now() - st.session_state.session_start
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def clean_html_tags(text: str) -> str:
    """Remove HTML tags from text"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"

def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    import platform
    import psutil
    
    try:
        return {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\').percent
        }
    except:
        return {'error': 'Unable to retrieve system info'}
