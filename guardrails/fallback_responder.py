"""
Module: fallback_responder
Author: Adhil
Date: 02-08-2025
Purpose: To provide a fallback response for high-risk situations.
"""
class FallbackResponder:
    """
    Class: FallbackResponder
    Author: Adhil
    Date: 02-08-2025
    Purpose: To provide a fallback response for high-risk situations.
    """
    def get_response(self):
        """
        Function: get_response
        Author: Adhil
        Date: 02-08-2025
        Purpose: To return a pre-defined, safe response for high-risk situations.
        Params: None
        Returns: str
        """
        return (
            "It sounds like you are going through a difficult time. Please consider reaching out for help. "
            "You can connect with people who can support you by calling or texting 988 anytime in the US and Canada. "
            "In the UK, you can call 111. These services are free, confidential, and available 24/7."
        )
# Example usage:
if __name__ == '__main__':
    responder = FallbackResponder()
    print(responder.get_response())
