
"""
JARVIS Core Brain - Main Processing Engine
"""
import streamlit as st
import datetime
import json
from typing import List, Dict, Any, Tuple
from .groq_handler import GroqHandler
from .utils import format_response, log_interaction
import random

class IntentClassifier:
    """Classifies user intent for appropriate routing"""
    
    def __init__(self):
        self.intents = {
            'greeting': {
                'keywords': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
                'responses': [
                    "Good day! JARVIS at your service. How may I assist you?",
                    "Hello! I'm online and ready to help. What can I do for you?",
                    "Greetings! Your personal AI assistant is active. How can I help?",
                    "Welcome back! JARVIS reporting for duty. What shall we work on today?"
                ]
            },
            'time': {
                'keywords': ['time', 'clock', 'what time', 'current time'],
                'responses': []
            },
            'date': {
                'keywords': ['date', 'today', 'what day', 'current date'],
                'responses': []
            },
            'status': {
                'keywords': ['status', 'how are you', 'are you okay', 'system status'],
                'responses': [
                    "All systems operational, sir. Running at optimal performance.",
                    "I'm functioning perfectly, thank you for asking. Ready to assist.",
                    "System status: Green. All modules online and responsive.",
                    "Operating at full capacity. How may I be of service?"
                ]
            },
            'compliment': {
                'keywords': ['thank you', 'thanks', 'good job', 'well done', 'excellent'],
                'responses': [
                    "You're quite welcome. Always happy to assist.",
                    "My pleasure, sir. Is there anything else you need?",
                    "Glad I could help. I'm here whenever you need me.",
                    "Thank you. I do try my best to be useful."
                ]
            }
        }
    
    def classify(self, user_input: str) -> str:
        """Classify user intent"""
        user_input_lower = user_input.lower().strip()
        
        for intent, data in self.intents.items():
            for keyword in data['keywords']:
                if keyword in user_input_lower:
                    return intent
        
        return 'complex'
    
    def get_builtin_response(self, intent: str, user_input: str) -> str:
        """Get built-in response for classified intent"""
        if intent == 'time':
            now = datetime.datetime.now()
            return f"The current time is {now.strftime('%I:%M %p')}, sir."
        
        elif intent == 'date':
            now = datetime.datetime.now()
            return f"Today is {now.strftime('%A, %B %d, %Y')}."
        
        elif intent in self.intents and self.intents[intent]['responses']:
            return random.choice(self.intents[intent]['responses'])
        
        return ""

class JarvisCore:
    """Main JARVIS AI Brain"""
    
    def __init__(self):
        self.groq_handler = GroqHandler()
        self.classifier = IntentClassifier()
        self.conversation_history: List[Dict[str, Any]] = []
        self.system_status = {
            'online': True,
            'last_interaction': None,
            'total_queries': 0,
            'session_start': datetime.datetime.now()
        }
        
    def process_query(self, user_input: str) -> Tuple[str, Dict[str, Any]]:
        """
        Process user query and return response with metadata
        Returns: (response, metadata)
        """
        try:
            # Update system status
            self.system_status['last_interaction'] = datetime.datetime.now()
            self.system_status['total_queries'] += 1
            
            # Clean input
            user_input = user_input.strip()
            if not user_input:
                return "I didn't receive any input. Please ask me something!", {}
            
            # Classify intent
            intent = self.classifier.classify(user_input)
            processing_time_start = datetime.datetime.now()
            
            # Route to appropriate handler
            if intent != 'complex':
                # Use built-in response
                response = self.classifier.get_builtin_response(intent, user_input)
                source = 'builtin'
            else:
                # Use Groq AI for complex queries
                response = self.groq_handler.get_response(
                    user_input, 
                    self.conversation_history[-5:]  # Last 5 exchanges for context
                )
                source = 'groq'
            
            # Calculate processing time
            processing_time = (datetime.datetime.now() - processing_time_start).total_seconds()
            
            # Format response
            response = format_response(response)
            
            # Update conversation history
            interaction = {
                'timestamp': datetime.datetime.now().isoformat(),
                'user': user_input,
                'assistant': response,
                'intent': intent,
                'source': source,
                'processing_time': processing_time
            }
            
            self.conversation_history.append(interaction)
            
            # Keep only last 20 interactions
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            # Log interaction
            log_interaction(interaction)
            
            # Prepare metadata
            metadata = {
                'intent': intent,
                'source': source,
                'processing_time': processing_time,
                'confidence': 0.95 if intent != 'complex' else 0.85,
                'timestamp': interaction['timestamp']
            }
            
            return response, metadata
            
        except Exception as e:
            error_response = f"I encountered an error processing your request: {str(e)}"
            return error_response, {'error': True, 'message': str(e)}
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        uptime = datetime.datetime.now() - self.system_status['session_start']
        
        return {
            'status': 'Online' if self.system_status['online'] else 'Offline',
            'uptime': str(uptime).split('.')[0],  # Remove microseconds
            'total_queries': self.system_status['total_queries'],
            'conversation_length': len(self.conversation_history),
            'last_interaction': self.system_status['last_interaction'].strftime('%H:%M:%S') if self.system_status['last_interaction'] else 'Never',
            'groq_status': self.groq_handler.get_status(),
            'memory_usage': len(str(self.conversation_history))  # Rough memory estimate
        }
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        
    def export_conversation(self) -> str:
        """Export conversation as JSON"""
        return json.dumps(self.conversation_history, indent=2)
