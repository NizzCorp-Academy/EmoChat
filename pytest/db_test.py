import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from db import models, connector


@patch.dict("os.environ", {
    "MYSQL_USER": "testuser",
    "MYSQL_PASSWORD": "testpass",
    "MYSQL_HOST": "localhost",
    "MYSQL_PORT": "3306",
    "MYSQL_DATABASE": "testdb"
})
@patch("db.connector.create_engine")
def test_initialize_database_success(mock_create_engine):
    # Mock engine behavior
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_create_engine.return_value = mock_engine
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    # Import the function after patching
    from db import connector
    connector.Base.metadata.create_all = MagicMock()
    
    connector.initialize_database()

    mock_conn.execute.assert_called_once()
    connector.Base.metadata.create_all.assert_called_once()

@patch.dict("os.environ", {
    "MYSQL_USER": "wrong",
    "MYSQL_PASSWORD": "wrong",
    "MYSQL_HOST": "localhost",
    "MYSQL_PORT": "3306",
    "MYSQL_DATABASE": "wrongdb"
})
@patch("db.connector.create_engine")
def test_initialize_database_operational_error(mock_create_engine):
    from sqlalchemy.exc import OperationalError
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = OperationalError("Test", None, None)
    mock_create_engine.return_value = mock_engine

    from db import connector
    with pytest.raises(OperationalError):
        connector.initialize_database()

def test_get_db_lifecycle():
    from db.connector import get_db
    session_gen = get_db()
    session = next(session_gen)
    assert session is not None
    assert hasattr(session, 'query')
    # Ensure session closes
    try:
        next(session_gen)
    except StopIteration:
        pass

@pytest.fixture(scope="module")
def test_db():
    # Use in-memory SQLite for isolated testing
    engine = create_engine("sqlite:///:memory:")
    models.Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine)
    yield TestingSession()
    clear_mappers()

def test_create_user(test_db):
    user = models.User(name="Alice", email="alice@example.com", hashed_password="hashed")
    test_db.add(user)
    test_db.commit()
    result = test_db.query(models.User).filter_by(email="alice@example.com").first()
    assert result.name == "Alice"

def test_create_chat_log(test_db):
    user = models.User(name="Bob", email="bob@example.com", hashed_password="hashed")
    test_db.add(user)
    test_db.commit()

    log = models.ChatLog(user_id=user.id, prompt="Hi", response="Hello!")
    test_db.add(log)
    test_db.commit()

    result = test_db.query(models.ChatLog).filter_by(user_id=user.id).first()
    assert result.response == "Hello!"

def test_create_feedback(test_db):
    user = models.User(name="Carol", email="carol@example.com", hashed_password="hashed")
    test_db.add(user)
    test_db.commit()

    log = models.ChatLog(user_id=user.id, prompt="Help", response="Sure")
    test_db.add(log)
    test_db.commit()

    feedback = models.Feedback(user_id=user.id, chat_log_id=log.id, rating=5, comment="Great")
    test_db.add(feedback)
    test_db.commit()

    result = test_db.query(models.Feedback).filter_by(user_id=user.id).first()
    assert result.rating == 5

def test_create_knowledge_base(test_db):
    kb = models.KnowledgeBase(title="Mental Health Tips", content_chunk="Stay hydrated.", tags="health")
    test_db.add(kb)
    test_db.commit()
    result = test_db.query(models.KnowledgeBase).first()
    assert result.title == "Mental Health Tips"

def test_create_vector_index(test_db):
    kb = models.KnowledgeBase(title="FAQ", content_chunk="What is AI?", tags="ai")
    test_db.add(kb)
    test_db.commit()

    vi = models.VectorIndex(vector_id="vec-123", document_id=kb.id, document_metadata="{}")
    test_db.add(vi)
    test_db.commit()

    result = test_db.query(models.VectorIndex).first()
    assert result.vector_id == "vec-123"