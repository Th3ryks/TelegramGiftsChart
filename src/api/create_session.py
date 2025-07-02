from pyrogram.client import Client
import os
from dotenv import load_dotenv

# ----- Constants -----
SESSION_NAME = "account"
ENV_VARS = {
    "API_ID": "API_ID",
    "API_HASH": "API_HASH",
    "PHONE_NUMBER": "PHONE_NUMBER"
}

# ----- Load environment variables -----
load_dotenv()

def get_env_var(name: str) -> str:
    """Get environment variable with error handling."""
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable {name} is not set")
    return value

# ----- Telegram API credentials -----
api_id = int(get_env_var(ENV_VARS["API_ID"]))
api_hash = get_env_var(ENV_VARS["API_HASH"])
phone_number = get_env_var(ENV_VARS["PHONE_NUMBER"])

# ----- Create and save session -----
app = Client(SESSION_NAME, api_id=api_id, api_hash=api_hash)

with app:
    print("Session created successfully!")