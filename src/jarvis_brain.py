
from .groq_handler import GroqHandler
from .builtin_responses import BuiltinResponses
from .intent_classifier import IntentClassifier
from .utils import format_response, log_interaction

class JarvisBrain:
    def __init__(self):
        self.groq = GroqHandler()
        self.builtin = BuiltinResponses()
        self.classifier = IntentClassifier()
        self.conversation_history = []
    
    def process_query(self, user_input):
        # Classify intent
        intent = self.classifier.classify(user_input)
        
        # Route to appropriate handler
        if intent in ['time', 'date', 'greeting', 'simple']:
            response = self.builtin.get_response(user_input, intent)
        else:
            response = self.groq.get_response(user_input, self.conversation_history)
        
        # Update history
        self.conversation_history.append({
            'user': user_input,
            'assistant': response,
            'intent': intent
        })
        
        # Log interaction
        log_interaction(user_input, response, intent)
        
        return format_response(response)
