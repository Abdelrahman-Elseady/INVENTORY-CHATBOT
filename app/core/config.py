import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROVIDER = os.getenv("PROVIDER")
    MODEL_NAME = os.getenv("MODEL_NAME")
    MODEL_API_KEY = os.getenv("MODEL_API_KEY")

settings = Settings()