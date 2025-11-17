import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")