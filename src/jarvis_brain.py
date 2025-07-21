
# Absolute imports instead of relative imports
from groq_handler import GroqHandler
from builtin_responses import BuiltinResponses
from intent_classifier import IntentClassifier
from utils import format_response, log_interaction

class JarvisBrain:
    def __init__(self):
        self.groq = GroqHandler()
        self.builtin = BuiltinResponses()
        self.classifier = IntentClassifier()
        self.conversation_history = []
    
    def process_query(self, user_input):
        """Main query processing method"""
        try:
            # Clean and validate input
            user_input = user_input.strip()
            if not user_input:
                return "I didn't receive any input. Please ask me something!"
            
            # Classify intent
            intent = self.classifier.classify(user_input)
            
            # Route to appropriate handler
            if intent in ['time', 'date', 'greeting', 'simple']:
                response = self.builtin.get_response(user_input, intent)
            else:
                response = self.groq.get_response(user_input, self.conversation_history)
            
            # Update conversation history
            self.conversation_history.append({
                'user': user_input,
                'assistant': response,
                'intent': intent
            })
            
            # Keep only last 10 exchanges
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            # Log interaction (optional)
            log_interaction(user_input, response, intent)
            
            return format_response(response)
            
        except Exception as e:
            return f"I encountered an error processing your request: {str(e)}"
