import sys
import os
import streamlit as st

# Add the project root directory to the Python path
# This ensures that the 'mindmate' package can be found
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from db.connector import initialize_database, get_db
from auth.auth_manager import AuthManager
from chatbot.llm_client import LLMClient
from chatbot.prompt_builder import PromptTemplateBuilder
from rag.rag_manager import RAGManager
from guardrails.guardrails_manager import GuardrailsManager
from feedback.chat_logger import ChatLogger
from feedback.feedback_handler import FeedbackHandler

# --- Database and App Initialization ---
initialize_database()

def render_login_page():
    """Renders the login and registration forms."""
    st.title("Welcome to EmoChat.ai")
    st.write("Your personal mental health companion.")

    db_session = next(get_db())
    auth_manager = AuthManager(db_session)

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                user = auth_manager.authenticate_user(email, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid email or password")

    with register_tab:
        with st.form("register_form"):
            name = st.text_input("Name")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_password")
            submitted = st.form_submit_button("Register")
            if submitted:
                user = auth_manager.create_user(name, email, password)
                if user:
                    st.session_state.user = user
                    st.success("Registration successful! Welcome to MindMate!")
                    st.rerun()
                else:
                    st.error("Registration failed. Email may already be in use.")

def render_chat_page():
    """Renders the main chat interface, sidebar, and logout button."""
    st.title("EmoChat.ai")

    # --- Sidebar for Chat History and Logout ---
    with st.sidebar:
        st.header(f"Welcome, {st.session_state.user.name}")
        
        # New Chat button
        if st.button("➕ New Chat", key="new_chat_button", use_container_width=True):
            # Clear current chat messages to start fresh
            st.session_state.messages = []
            if 'last_log_id' in st.session_state:
                del st.session_state['last_log_id']
            st.rerun()
        
        st.markdown("---")  # Separator line
        
        st.subheader("Chat History")
        chat_history = st.session_state.chat_logger.get_chat_history(st.session_state.user.id)
        
        # --- Display Chat History ---
        for chat in chat_history:
            with st.container():
                if st.button(f"📜 {chat.prompt[:30]}...", key=f"ch_{chat.id}", use_container_width=True):
                    # When a historical chat is clicked, load its messages
                    st.session_state.messages = [
                        {"role": "user", "content": chat.prompt},
                        {"role": "assistant", "content": chat.response}
                    ]
                    if 'last_log_id' in st.session_state:
                        del st.session_state['last_log_id']
                    st.rerun()
        
        # Add some space to push logout button to bottom
        st.write("")
        st.write("")
        
        # Logout button at the bottom
        if st.button("🚪 Logout", key="logout_button", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # --- Main Chat Interface ---
    db_session = next(get_db())

    # Initialize chat message history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept and process user input
    if prompt := st.chat_input("How are you feeling today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            guardrails_response = st.session_state.guardrails_manager.check_and_respond(prompt)

            if guardrails_response:
                full_response = guardrails_response
                message_placeholder.markdown(full_response)
            else:
                message_placeholder.markdown("Thinking...")
                retrieved_context = st.session_state.rag_manager.get_context(prompt)
                full_prompt = st.session_state.prompt_builder.build(prompt, context=retrieved_context)
                response_stream = st.session_state.llm_client.get_response_stream(full_prompt)
                full_response = message_placeholder.write_stream(response_stream)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Log interaction
        log_entry = st.session_state.chat_logger.log_interaction(
            user_id=st.session_state.user.id,
            prompt=prompt,
            response=full_response,
            risk_flag=bool(guardrails_response)
        )
        st.session_state.last_log_id = log_entry.id

        # Add feedback mechanism
        # (This could be refactored into its own function for clarity)

    if 'last_log_id' in st.session_state and st.session_state.last_log_id:
        st.markdown("---")
        st.write("How was this response?")
        col1, col2 = st.columns(2)
        if col1.button("👍", key=f"thumbs_up_{st.session_state.last_log_id}"):
            st.session_state.feedback_handler.save_feedback(st.session_state.user.id, st.session_state.last_log_id, 5, "Positive")
            st.success("Thanks for your feedback!")
            st.session_state.last_log_id = None
            st.rerun()
        if col2.button("👎", key=f"thumbs_down_{st.session_state.last_log_id}"):
            st.session_state.feedback_handler.save_feedback(st.session_state.user.id, st.session_state.last_log_id, 1, "Negative")
            st.success("Thanks for your feedback!")
            st.session_state.last_log_id = None
            st.rerun()

def main():
    """Main function to control page rendering."""
    if 'user' not in st.session_state or st.session_state.user is None:
        render_login_page()
    else:
        db_session = next(get_db())
        # Initialize chat components if they don't exist
        if 'llm_client' not in st.session_state:
            st.session_state.llm_client = LLMClient()
        if 'prompt_builder' not in st.session_state:
            st.session_state.prompt_builder = PromptTemplateBuilder()
        if 'rag_manager' not in st.session_state:
            st.session_state.rag_manager = RAGManager(db_session)
        if 'guardrails_manager' not in st.session_state:
            st.session_state.guardrails_manager = GuardrailsManager()
        if 'chat_logger' not in st.session_state:
            st.session_state.chat_logger = ChatLogger(db_session)
        if 'feedback_handler' not in st.session_state:
            st.session_state.feedback_handler = FeedbackHandler(db_session)
        render_chat_page()

if __name__ == "__main__":
    main()
