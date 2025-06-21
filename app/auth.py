import streamlit as st
import hashlib

REQUIRED_API_KEY = "open-2025"

USER_CREDENTIALS = {
    "demo": hashlib.sha256("demo123".encode()).hexdigest(),
    "admin": hashlib.sha256("adminpass".encode()).hexdigest()
}

def login():
    if "api_valid" not in st.session_state:
        st.session_state.api_valid = False
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if "username" not in st.session_state:
        st.session_state.username = None

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

    if not st.session_state.auth:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            if USER_CREDENTIALS.get(username) == hashed_pw:
                st.session_state.auth = True
                st.session_state.username = username
                st.success("Logged in.")
                st.rerun()
            else:
                st.error("Invalid credentials.")
        st.stop()

    if st.session_state.username and "display_name" not in st.session_state:
        st.title("Welcome")
        name = st.text_input("What name would you like to use in this session?")
        if st.button("Continue"):
            if name.strip():
                st.session_state.display_name = name.strip()
                st.success(f"Hello, {st.session_state.display_name}!")
                st.rerun()
        st.stop()
