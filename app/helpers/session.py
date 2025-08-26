# ===========================================================
# Session Related Functions
# ===========================================================

from dotenv import load_dotenv
from os import getenv
from datetime import timedelta


# -----------------------------------------------------------
# Load the session key from .env and set it for the app
# -----------------------------------------------------------
def init_session(app):
    load_dotenv()
    SESSION_KEY = getenv("SESSION_KEY")
    app.secret_key = SESSION_KEY
    app.permanent_session_lifetime = timedelta(days=30)
