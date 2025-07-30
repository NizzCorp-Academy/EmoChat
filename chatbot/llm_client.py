import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_url = os.getenv("LM_STUDIO_API_URL")
        self.model_name = os.getenv("LM_STUDIO_MODEL_NAME")
        
        if not self.api_url or not self.model_name:
            raise ValueError("LM Studio API URL or model name not found in .env file")

        self.llm = ChatOpenAI(
            model=self.model_name,
            base_url=self.api_url,
            api_key="lm-studio", # Required by langchain but not used by LM Studio
            temperature=0.5
        )

    def get_response_stream(self, prompt_text):
        """
        Gets a streaming response from the LLM for a single prompt.

        Args:
            prompt_text: The user's prompt as a string.

        Returns:
            An iterator of response string chunks.
        """
        try:
            # self.llm.stream returns AIMessageChunk objects.
            # We need to iterate through them and yield the string content.
            for chunk in self.llm.stream(prompt_text):
                yield chunk.content
        except Exception as e:
            print(f"Error getting streaming response from LLM: {e}")
            # In case of an error, yield a single message chunk to display to the user.
            yield "Sorry, I'm having trouble connecting to my brain right now."

# Example usage:
if __name__ == '__main__':
    client = LLMClient()
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    response_stream = client.get_response_stream(messages)
    response = ""
    for chunk in response_stream:
        print(chunk, end="", flush=True)
        response += chunk
    print() # Newline after stream
    # print(response) # You can uncomment this to see the full response at once
