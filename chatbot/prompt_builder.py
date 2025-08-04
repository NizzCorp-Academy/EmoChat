"""
Module: prompt_builder
Author: Arshad
Date: 28-07-2025
Purpose: To provide a builder for creating prompt templates.
"""

class PromptTemplateBuilder:
    """
    Class: PromptTemplateBuilder
    Author: Arshad
    Date: 28-07-2025
    Purpose: A builder for creating prompt templates.
    """
    def __init__(self):
        """
        Function: __init__
        Author: Arshad
        Date: 28-07-2025
        Purpose: To initialize the PromptTemplateBuilder.
        Params: None
        Returns: None
        """
        # In the future, this could load templates from files
        self.system_prompt = "You are EcoChat, a compassionate and supportive AI assistant. Your goal is to provide a safe space for users to express their thoughts and feelings. Be empathetic, non-judgmental, and helpful."

    def build(self, user_message, context=None):
        """
        Function: build
        Author: Arshad
        Date: 29-07-2025
        Purpose: To build a complete prompt from a user message and optional context.
        Params: str user_message, str context
        Returns: str
        """
        full_prompt = f"System: {self.system_prompt}\n"
        if context:
            full_prompt += f"Context: {context}\n"
        full_prompt += f"User: {user_message}\nAssistant:"
        return full_prompt

# Example usage:
if __name__ == '__main__':
    builder = PromptTemplateBuilder()
    prompt = builder.build("I'm feeling a bit down today.")
    print(prompt)
