import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

APP_KEY = os.getenv("APP_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
GATEWAY_ADDRESS = os.getenv("GATEWAY_ADDRESS")