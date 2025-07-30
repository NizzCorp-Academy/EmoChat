class PromptTemplateBuilder:
    def __init__(self):
        # In the future, this could load templates from files
        self.system_prompt = "You are MindMate, a compassionate and supportive AI assistant. Your goal is to provide a safe space for users to express their thoughts and feelings. Be empathetic, non-judgmental, and helpful."

    def build(self, user_message, context=None):
        """
        Builds a complete prompt from a user message and optional context.
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
