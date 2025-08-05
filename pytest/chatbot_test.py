import pytest
from unittest.mock import patch, MagicMock
import os
from prompt_builder import PromptTemplateBuilder

# Patch ChatOpenAI before importing the module
@patch.dict(os.environ, {
    "LM_STUDIO_API_URL": "http://localhost:1234",
    "LM_STUDIO_MODEL_NAME": "gpt-neo"
})
@patch("llm_client.ChatOpenAI")
def test_llm_client_initialization(mock_chat_openai):
    from llm_client import LLMClient
    client = LLMClient()
    assert client.api_url == "http://localhost:1234"
    assert client.model_name == "gpt-neo"
    mock_chat_openai.assert_called_once()

@patch.dict(os.environ, {
    "LM_STUDIO_API_URL": "",
    "LM_STUDIO_MODEL_NAME": ""
})
def test_llm_client_missing_env_vars():
    with pytest.raises(ValueError):
        from llm_client import LLMClient
        LLMClient()

@patch.dict(os.environ, {
    "LM_STUDIO_API_URL": "http://localhost:1234",
    "LM_STUDIO_MODEL_NAME": "gpt-neo"
})
@patch("llm_client.ChatOpenAI")
def test_llm_client_response_stream_success(mock_chat_openai):
    from llm_client import LLMClient

    mock_chunk = MagicMock()
    mock_chunk.content = "Hello, "
    mock_llm_instance = MagicMock()
    mock_llm_instance.stream.return_value = [mock_chunk, mock_chunk]
    mock_chat_openai.return_value = mock_llm_instance

    client = LLMClient()
    response = list(client.get_response_stream([{"role": "user", "content": "Hi"}]))
    assert response == ["Hello, ", "Hello, "]

@patch.dict(os.environ, {
    "LM_STUDIO_API_URL": "http://localhost:1234",
    "LM_STUDIO_MODEL_NAME": "gpt-neo"
})
@patch("llm_client.ChatOpenAI")
def test_llm_client_response_stream_error(mock_chat_openai):
    from llm_client import LLMClient

    mock_llm_instance = MagicMock()
    mock_llm_instance.stream.side_effect = Exception("Connection error")
    mock_chat_openai.return_value = mock_llm_instance

    client = LLMClient()
    response = list(client.get_response_stream([{"role": "user", "content": "Hi"}]))
    assert response == ["Sorry, I'm having trouble connecting to my brain right now."]

import pytest
from prompt_builder import PromptTemplateBuilder

def test_prompt_builder_default_prompt():
    builder = PromptTemplateBuilder()
    result = builder.build("Hello!")
    assert "System: You are EcoChat" in result
    assert "User: Hello!" in result
    assert result.endswith("Assistant:")

def test_prompt_builder_with_context():
    builder = PromptTemplateBuilder()
    result = builder.build("Hello!", context="Previous message was ignored.")
    assert "Context: Previous message was ignored." in result
