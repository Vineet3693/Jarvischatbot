
class IntentClassifier:
    def __init__(self):
        self.intent_keywords = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            'time': ['time', 'clock', 'what time'],
            'date': ['date', 'today', 'what day'],
            'simple': ['ok', 'okay', 'yes', 'no', 'thanks', 'thank you']
        }
    
    def classify(self, user_input):
        user_input_lower = user_input.lower()
        
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return intent
        
        return 'complex'  # Default to Groq AI for complex queries
