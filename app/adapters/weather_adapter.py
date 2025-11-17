import httpx
from app.config import OPEN_WEATHER_API_KEY

class WeatherAdapter:
    """
    Adapter class for interacting with the OpenWeatherMap API.

    This class provides an asynchronous method to fetch current weather data for a given city
    using the OpenWeatherMap API.

    Attributes:
        BASE_URL (str): The base URL for the OpenWeatherMap API.
        api_key (str): The API key used for authenticating requests.
    """
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.api_key = OPEN_WEATHER_API_KEY
        if not self.api_key:
            raise ValueError("API key for OpenWeatherMap is not set in environment variables.")

    async def get_weather(self, city: str) -> dict:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        timeout = httpx.Timeout(5.0, connect=3.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                if e.response.status_code == 404:
                    raise ValueError(f"City '{city}' not found in OpenWeather API")
                elif e.response.status_code == 401:
                    raise ValueError("Invalid or missing API key for OpenWeather API")
                else:
                    raise RuntimeError(f"OpenWeather API returned {e.response.status_code} error: {e.response.text}")
            except httpx.RequestError as e:
                raise ConnectionError(f"Error connecting to OpenWeather API: {str(e)}")