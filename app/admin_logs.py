import streamlit as st
import os

LOG_DIR = "logs"

def show_admin_logs(username: str):
    if username != "admin":
        st.warning("Access denied. Admin only.")
        return

    st.title("📜 Audit Log Viewer")

    log_files = sorted([f for f in os.listdir(LOG_DIR) if f.endswith(".log")], reverse=True)

    if not log_files:
        st.info("No logs found.")
        return

    selected_log = st.selectbox("Select log file", log_files)
    keyword = st.text_input("Filter by keyword (optional)")

    with open(os.path.join(LOG_DIR, selected_log), "r") as f:
        lines = f.readlines()

    if keyword:
        lines = [line for line in lines if keyword.lower() in line.lower()]

    st.code("".join(lines[-100:]), language="text")
