import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from auth import AuthManager
from passlib.context import CryptContext
from unittest.mock import MagicMock
from db.models import User

# Sample password context from original module
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def auth_manager(mock_db_session):
    return AuthManager(mock_db_session)

def test_get_password_hash(auth_manager):
    password = "securepassword"
    hashed = auth_manager.get_password_hash(password)
    assert pwd_context.verify(password, hashed)

def test_verify_password(auth_manager):
    password = "mypassword"
    hashed = auth_manager.get_password_hash(password)
    assert auth_manager.verify_password(password, hashed)
    assert not auth_manager.verify_password("wrongpassword", hashed)

def test_get_user_found(auth_manager, mock_db_session):
    fake_user = MagicMock(spec=User)
    mock_db_session.query.return_value.filter.return_value.first.return_value = fake_user

    user = auth_manager.get_user("test@example.com")
    assert user == fake_user

def test_get_user_not_found(auth_manager, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    user = auth_manager.get_user("notfound@example.com")
    assert user is None

def test_create_user_success(auth_manager, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    name = "Alice"
    email = "alice@example.com"
    password = "alice123"

    user_instance = User(name=name, email=email, hashed_password="hashed")
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    # Patch User creation
    def user_constructor(name, email, hashed_password):
        return user_instance
    auth_manager.get_password_hash = MagicMock(return_value="hashed")
    auth_manager.get_user = MagicMock(return_value=None)

    # Replace actual User instantiation with our mock
    from db import models
    models.User = user_constructor

    created_user = auth_manager.create_user(name, email, password)

    assert created_user == user_instance
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(user_instance)

def test_create_user_existing(auth_manager):
    auth_manager.get_user = MagicMock(return_value=MagicMock(spec=User))
    result = auth_manager.create_user("Bob", "bob@example.com", "secret")
    assert result is None

def test_authenticate_user_success(auth_manager):
    email = "john@example.com"
    password = "password123"
    hashed_password = pwd_context.hash(password)

    fake_user = MagicMock(spec=User)
    fake_user.hashed_password = hashed_password

    auth_manager.get_user = MagicMock(return_value=fake_user)
    auth_manager.verify_password = MagicMock(return_value=True)

    user = auth_manager.authenticate_user(email, password)
    assert user == fake_user

def test_authenticate_user_user_not_found(auth_manager):
    auth_manager.get_user = MagicMock(return_value=None)
    result = auth_manager.authenticate_user("unknown@example.com", "pass")
    assert result is None

def test_authenticate_user_wrong_password(auth_manager):
    fake_user = MagicMock(spec=User)
    fake_user.hashed_password = pwd_context.hash("correctpassword")

    auth_manager.get_user = MagicMock(return_value=fake_user)
    auth_manager.verify_password = MagicMock(return_value=False)

    result = auth_manager.authenticate_user("user@example.com", "wrongpass")
    assert result is None
