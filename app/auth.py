import streamlit as st
import hashlib

REQUIRED_API_KEY = "open-access-2025"

USER_CREDENTIALS = {
    "user": hashlib.sha256("user123".encode()).hexdigest()
}

def login():
    if "api_valid" not in st.session_state:
        st.session_state.api_valid = False
    if "auth" not in st.session_state:
        st.session_state.auth = False

    # API Key validation
    if not st.session_state.api_valid:
        st.title("Enter API Key")
        api_input = st.text_input("API Key", type="password")
        if st.button("Validate"):
            if api_input == REQUIRED_API_KEY:
                st.session_state.api_valid = True
                st.success("API key accepted.")
                st.rerun()
            else:
                st.error("Invalid API key.")
        st.stop()

    # Authentication
    if not st.session_state.auth:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            if USER_CREDENTIALS.get(username) == hashed_pw:
                st.session_state.auth = True
                st.success("Logged in successfully.")
                st.rerun()
            else:
                st.error("Invalid credentials.")
        st.stop()
