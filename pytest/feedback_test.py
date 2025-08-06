import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import models
from chat_logger import ChatLogger
from feedback_handler import FeedbackHandler

# ---------- Pytest Fixtures ----------

@pytest.fixture(scope="module")
def engine():
    return create_engine("sqlite:///:memory:", echo=False)

@pytest.fixture(scope="module")
def tables(engine):
    models.Base.metadata.create_all(bind=engine)
    return

@pytest.fixture
def db_session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def test_user(db_session):
    user = models.User(name="Test User", email="test@example.com", hashed_password="hashed")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_chat_log(db_session, test_user):
    log = models.ChatLog(user_id=test_user.id, prompt="Hi", response="Hello!")
    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)
    return log

# ---------- ChatLogger Tests ----------

def test_log_interaction_creates_entry(db_session, test_user):
    logger = ChatLogger(db_session)
    log = logger.log_interaction(test_user.id, "What's up?", "All good!", risk_flag=True)
    
    assert log.id is not None
    assert log.user_id == test_user.id
    assert log.risk_flag is True
    assert log.prompt == "What's up?"

def test_get_chat_history_returns_all_sorted(db_session, test_user):
    logger = ChatLogger(db_session)
    # Add multiple logs
    logger.log_interaction(test_user.id, "1", "A")
    logger.log_interaction(test_user.id, "2", "B")
    logger.log_interaction(test_user.id, "3", "C")

    history = logger.get_chat_history(test_user.id)
    prompts = [chat.prompt for chat in history]
    assert prompts == ["1", "2", "3"]

# ---------- FeedbackHandler Tests ----------

def test_save_feedback_creates_entry(db_session, test_user, test_chat_log):
    handler = FeedbackHandler(db_session)
    feedback = handler.save_feedback(test_user.id, test_chat_log.id, rating=4, comment="Nice job!")

    assert feedback.id is not None
    assert feedback.user_id == test_user.id
    assert feedback.chat_log_id == test_chat_log.id
    assert feedback.rating == 4
    assert feedback.comment == "Nice job!"
