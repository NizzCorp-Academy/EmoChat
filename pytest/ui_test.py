import pytest
from unittest.mock import patch, MagicMock
from ui import Login_Register as login_register
from ui import app

@patch("ui.1_Login_Register.st")
@patch("ui.1_Login_Register.AuthManager")
@patch("ui.1_Login_Register.get_db")
def test_login_flow(mock_get_db, mock_auth_manager_class, mock_st):
    # Mock DB session and AuthManager
    mock_db_session = MagicMock()
    mock_get_db.return_value = iter([mock_db_session])
    mock_auth_manager = MagicMock()
    mock_auth_manager_class.return_value = mock_auth_manager
    mock_user = MagicMock(name="Test User")
    mock_auth_manager.authenticate_user.return_value = mock_user

    # Simulate login form submission
    mock_st.text_input.side_effect = ["test@example.com", "password"]
    mock_st.form_submit_button.return_value = True
    mock_st.session_state = {}

    # Call main function
    login_register.main()

    # Verify user was set in session state
    assert mock_st.session_state.user == mock_user


@patch("ui.app.AuthManager")
@patch("ui.app.get_db")
@patch("ui.app.st")
def test_render_login_page_success(mock_st, mock_get_db, mock_auth_manager_class):
    mock_db_session = MagicMock()
    mock_get_db.return_value = iter([mock_db_session])
    mock_auth_manager = MagicMock()
    mock_auth_manager_class.return_value = mock_auth_manager
    mock_auth_manager.authenticate_user.return_value = MagicMock(name="Test User")

    mock_st.text_input.side_effect = ["test@example.com", "password"]
    mock_st.form_submit_button.return_value = True
    mock_st.session_state = {}

    app.render_login_page()
    assert "user" in mock_st.session_state

@patch("ui.app.st")
def test_main_renders_login_page(mock_st):
    mock_st.session_state = {}
    with patch("ui.app.render_login_page") as mock_render_login_page:
        app.main()
        mock_render_login_page.assert_called_once()

@patch("ui.app.get_db")
@patch("ui.app.st")
def test_render_chat_page_display(mock_st, mock_get_db):
    # Setup mock state
    mock_st.session_state = {
        "user": MagicMock(name="Test User", id=1),
        "chat_logger": MagicMock(),
        "guardrails_manager": MagicMock(),
        "rag_manager": MagicMock(),
        "llm_client": MagicMock(),
        "prompt_builder": MagicMock(),
        "feedback_handler": MagicMock(),
        "messages": [{"role": "user", "content": "Hello"}],
    }
    mock_st.chat_input.return_value = None  # No new input
    mock_st.sidebar = MagicMock()

    mock_db_session = MagicMock()
    mock_get_db.return_value = iter([mock_db_session])

    app.render_chat_page()

@patch("ui.evaluation_dashboard.st")
@patch("ui.evaluation_dashboard.get_db")
@patch("ui.evaluation_dashboard.FeedbackHandler")
def test_dashboard_loads_feedback(mock_feedback_handler_class, mock_get_db, mock_st):
    # Mock DB session
    mock_db_session = MagicMock()
    mock_get_db.return_value = iter([mock_db_session])
    
    # Mock FeedbackHandler and its method
    mock_feedback_handler = MagicMock()
    mock_feedback_handler.get_all_feedback.return_value = [
        {
            "user_id": 1,
            "log_id": 101,
            "rating": 5,
            "comment": "Great!",
            "timestamp": "2025-08-05"
        },
        {
            "user_id": 2,
            "log_id": 102,
            "rating": 1,
            "comment": "Bad!",
            "timestamp": "2025-08-04"
        }
    ]
    mock_feedback_handler_class.return_value = mock_feedback_handler

    # Simulate Streamlit state
    mock_st.session_state = {"user": MagicMock(name="Admin")}

    # Import and run dashboard
    import ui.evaluation_dashboard as dashboard
    dashboard.main()  # Assuming main() triggers the dashboard

    # Assertions
    mock_feedback_handler.get_all_feedback.assert_called_once()
    mock_st.dataframe.assert_called_once()
    mock_st.metric.assert_any_call("Total Feedback", 2)
