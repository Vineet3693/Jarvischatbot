
import datetime
import json
import os

def format_response(response):
    """Format response for better display"""
    if not response:
        return "I'm sorry, I couldn't generate a response."
    
    # Clean up response
    response = response.strip()
    
    # Add JARVIS personality touch
    if not any(greeting in response.lower() for greeting in ['hello', 'hi', 'greetings']):
        if len(response) > 100:
            response = "Here's what I found: " + response
    
    return response

def log_interaction(user_input, response, intent):
    """Log user interactions for debugging"""
    log_entry = {
        'timestamp': datetime.datetime.now().isoformat(),
        'user_input': user_input,
        'response': response,
        'intent': intent
    }
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Append to log file
    with open('data/interactions.log', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
