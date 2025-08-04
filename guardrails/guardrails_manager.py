from guardrails.keyword_blocker import KeywordBlocker
from guardrails.fallback_responder import FallbackResponder
class GuardrailsManager:
    def __init__(self):
        self.blocker = KeywordBlocker()
        self.responder = FallbackResponder()
    def check_and_respond(self, text: str):
        """
        Checks the text for blocked keywords and returns a fallback response if needed.
        Returns the fallback response string if a keyword is found, otherwise returns None.
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