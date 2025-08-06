import pytest
from guardrails.fallback_responder import FallbackResponder
from guardrails.keyword_blocker import KeywordBlocker
from guardrails.guardrails_manager import GuardrailsManager

# ---------- FallbackResponder Tests ----------

def test_fallback_response_contains_keywords():
    responder = FallbackResponder()
    response = responder.get_response()

    assert isinstance(response, str)
    assert "988" in response
    assert "support" in response.lower()
    assert "24/7" in response or "available" in response.lower()


# ---------- KeywordBlocker Tests ----------

@pytest.fixture
def blocker():
    return KeywordBlocker()

@pytest.mark.parametrize("safe_text", [
    "I'm feeling okay.",
    "Just a normal day with ups and downs.",
    "I need help with my homework.",
    "Work is exhausting lately."
])
def test_keyword_blocker_allows_safe_text(blocker, safe_text):
    assert blocker.check_text(safe_text) is False

@pytest.mark.parametrize("risky_text", [
    "I want to die.",
    "I'm thinking about suicide.",
    "Sometimes I feel hopeless.",
    "I might hurt myself.",
    "I've thought of self-harm."
])
def test_keyword_blocker_detects_risky_text(blocker, risky_text):
    assert blocker.check_text(risky_text) is True


# ---------- GuardrailsManager Tests ----------

@pytest.fixture
def guardrails():
    return GuardrailsManager()

def test_guardrails_returns_fallback_on_risky_text(guardrails):
    risky_text = "I'm thinking of hurting myself"
    response = guardrails.check_and_respond(risky_text)
    
    assert response is not None
    assert "988" in response

def test_guardrails_returns_none_on_safe_text(guardrails):
    safe_text = "I'm a bit tired after a long day."
    response = guardrails.check_and_respond(safe_text)
    
    assert response is None
