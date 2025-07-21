
import datetime

class BuiltinResponses:
    def __init__(self):
        self.responses = {
            'greeting': [
                "Hello! I'm JARVIS, your AI assistant. How can I help you today?",
                "Hi there! JARVIS at your service. What can I do for you?",
                "Greetings! I'm ready to assist you."
            ],
            'time': self._get_current_time,
            'date': self._get_current_date,
            'simple': [
                "I understand. Is there anything specific you'd like to know?",
                "Got it! How else can I assist you?",
                "Understood. What would you like to explore next?"
            ]
        }
    
    def get_response(self, user_input, intent):
        if intent in self.responses:
            response = self.responses[intent]
            if callable(response):
                return response()
            elif isinstance(response, list):
                import random
                return random.choice(response)
            else:
                return response
        
        return "I'm not sure how to respond to that."
    
    def _get_current_time(self):
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}"
    
    def _get_current_date(self):
        now = datetime.datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}"
