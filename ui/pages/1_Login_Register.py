"""
Module: 1_Login_Register
Author: Arshad
Date: 02-08-2025
Purpose: To provide the login and registration page for the Streamlit UI.
"""
import streamlit as st
from auth.auth_manager import AuthManager
from db.connector import get_db

def main():
    """
    Function: main
    Author: Arshad
    Date: 03-08-2025
    Purpose: Main function to control page rendering.
    Params: None
    Returns: None
    """
    st.title("Login / Register")

    if 'user' in st.session_state and st.session_state.user is not None:
        st.success(f"Welcome back, {st.session_state.user.name}!")
        if st.button("Logout"):
            del st.session_state.user
            st.rerun()
        return

    db_session = next(get_db())
    auth_manager = AuthManager(db_session)

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form"):
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login")

            if submitted:
                user = auth_manager.authenticate_user(email, password)
                if user:
                    st.session_state.user = user
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

    with register_tab:
        with st.form("register_form"):
            st.subheader("Register")
            name = st.text_input("Name", key="register_name")
            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")
            submitted = st.form_submit_button("Register")

            if submitted:
                if not name or not email or not password:
                    st.error("All fields are required.")
                else:
                    user = auth_manager.create_user(name, email, password)
                    if user:
                        st.success("Registration successful! Please log in.")
                    else:
                        st.error("An account with this email already exists.")

if __name__ == "__main__":
    main()
