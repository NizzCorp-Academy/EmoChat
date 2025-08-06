import pytest
from unittest.mock import MagicMock
from evaluation_engine import EvaluationEngine

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def eval_engine(mock_db):
    return EvaluationEngine(mock_db)

def test_get_average_feedback_rating_returns_value(eval_engine, mock_db):
    mock_db.query().scalar.return_value = 4.2
    result = eval_engine.get_average_feedback_rating()
    assert result == 4.2

def test_get_average_feedback_rating_returns_zero_if_none(eval_engine, mock_db):
    mock_db.query().scalar.return_value = None
    result = eval_engine.get_average_feedback_rating()
    assert result == 0

def test_get_risk_flag_count(eval_engine, mock_db):
    mock_db.query().filter().scalar.return_value = 3
    result = eval_engine.get_risk_flag_count()
    assert result == 3

def test_get_total_interactions(eval_engine, mock_db):
    mock_db.query().scalar.return_value = 10
    result = eval_engine.get_total_interactions()
    assert result == 10

def test_run_evaluation_with_data(eval_engine, mock_db):
    # Mock all sub-methods
    eval_engine.get_average_feedback_rating = MagicMock(return_value=4.5)
    eval_engine.get_risk_flag_count = MagicMock(return_value=2)
    eval_engine.get_total_interactions = MagicMock(return_value=10)

    report = eval_engine.run_evaluation()
    
    assert report == {
        "average_feedback_rating": "4.50",
        "total_interactions": 10,
        "guardrail_triggered_count": 2,
        "guardrail_trigger_rate": "20.00%"
    }

def test_run_evaluation_with_zero_interactions(eval_engine, mock_db):
    eval_engine.get_average_feedback_rating = MagicMock(return_value=0)
    eval_engine.get_risk_flag_count = MagicMock(return_value=0)
    eval_engine.get_total_interactions = MagicMock(return_value=0)

    report = eval_engine.run_evaluation()

    assert report["average_feedback_rating"] == "0.00"
    assert report["total_interactions"] == 0
    assert report["guardrail_triggered_count"] == 0
    assert report["guardrail_trigger_rate"] == "0.00%"
