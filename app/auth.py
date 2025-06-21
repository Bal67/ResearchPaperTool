import streamlit as st
import hashlib

USER_CREDENTIALS = {
    "demo": hashlib.sha256("demo123".encode()).hexdigest()
}

def login():
    if "auth" not in st.session_state:
        st.session_state.auth = False

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
                st.error("Invalid credentials")
        st.stop()
