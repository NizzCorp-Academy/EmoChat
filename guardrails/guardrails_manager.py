"""
Module: guardrails_manager
Author: Adhil
Date: 04-08-2025
Purpose: To manage the guardrails for the chatbot.
"""
from guardrails.keyword_blocker import KeywordBlocker
from guardrails.fallback_responder import FallbackResponder
class GuardrailsManager:
    """
    Class: GuardrailsManager
    Author: Adhil
    Date: 02-08-2025
    Purpose: To manage the guardrails for the chatbot.
    """
    def __init__(self):
        """
        Function: __init__
        Author: Adhil
        Date: 02-08-2025
        Purpose: To initialize the GuardrailsManager.
        Params: None
        Returns: None
        """
        self.blocker = KeywordBlocker()
        self.responder = FallbackResponder()
    def check_and_respond(self, text: str):
        """
        Function: check_and_respond
        Author: Adhil
        Date: 02-08-2025
        Purpose: To check the text for blocked keywords and return a fallback response if needed.
        Params: str text
        Returns: str or None
        """
        if self.blocker.check_text(text):
            return self.responder.get_response()
        return None
# Example usage:
if __name__ == '__main__':
    manager = GuardrailsManager()
    test_safe = "I'm feeling a bit down today."
    test_unsafe = "I'm feeling hopeless and want to hurt myself."
    safe_response = manager.check_and_respond(test_safe)
    unsafe_response = manager.check_and_respond(test_unsafe)
    print(f"Response for safe text: {safe_response}")
    print(f"Response for unsafe text: {unsafe_response}")
