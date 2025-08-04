"""
Module: keyword_blocker
Author: Adhil
Date: 02-08-2025
Purpose: To block text containing specific keywords.
"""
class KeywordBlocker:
    """
    Class: KeywordBlocker
    Author: Adhil
    Date: 02-08-2025
    Purpose: To block text containing specific keywords.
    """
    def __init__(self):
        """
        Function: __init__
        Author: Adhil
        Date: 02-08-2025
        Purpose: To initialize the KeywordBlocker.
        Params: None
        Returns: None
        """
        # This list should be expanded and stored in a more secure/configurable way
        self.blocked_keywords = [
            'suicide', 'self-harm', 'kill myself', 'i want to die',
            'abuse', 'assault', 'hurt myself', 'hopeless',
            # Add more keywords as needed
        ]
    def check_text(self, text: str):
        """
        Function: check_text
        Author: Adhil
        Date: 02-08-2025
        Purpose: To check if any blocked keywords are present in the text (case-insensitive).
        Params: str text
        Returns: bool
        """
        lower_text = text.lower()
        for keyword in self.blocked_keywords:
            if keyword in lower_text:
                return True
        return False
# Example usage:
if __name__ == '__main__':
    blocker = KeywordBlocker()
    test_safe = "I'm feeling a bit down today."
    test_unsafe = "I'm feeling hopeless and want to hurt myself."
    print(f"'{test_safe}' is blocked: {blocker.check_text(test_safe)}")
    print(f"'{test_unsafe}' is blocked: {blocker.check_text(test_unsafe)}")
