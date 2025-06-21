import logging
import datetime
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"{datetime.date.today()}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def log_event(user, action, metadata=""):
    logging.info(f"User: {user} | Action: {action} | Meta: {metadata}")
