class FallbackResponder:
    def get_response(self):
        """
        Returns a pre-defined, safe response for high-risk situations.
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