import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
SERVER_PORT = os.getenv("SERVER_PORT" or "50051")
UPSTREAM_SERVICE_URL = os.getenv("UPSTREAM_SERVICE_URL" or "http://api.openweathermap.org/data/2.5/weather")
API_KEY = os.getenv("API_KEY")
SERVER_ADDR = os.getenv("SERVER_ADDR" or "localhost:50051")
SERVER_TIMEOUT= float(os.getenv("SERVER_TIMEOUT" or "5.0"))