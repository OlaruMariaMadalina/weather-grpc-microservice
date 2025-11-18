import httpx
from app.config import OPEN_WEATHER_API_KEY, UPSTREAM_SERVICE_URL
from app.exceptions.weather_exceptions import (
    CityNotFoundError,
    InvalidUpstreamApiKeyError,
    UpstreamUnavailableError,
    UpstreamBadResponseError,
)

class WeatherAdapter:
    """
    Adapter class for interacting with the OpenWeatherMap API.

    This class provides an asynchronous method to fetch current weather data for a given city
    using the OpenWeatherMap API.

    Attributes:
        BASE_URL (str): The base URL for the OpenWeatherMap API.
        api_key (str): The API key used for authenticating requests.
    """

    def __init__(self):
        self.api_key = OPEN_WEATHER_API_KEY
        if not self.api_key:
            raise InvalidUpstreamApiKeyError("OpenWeatherMap API key is missing")

    async def get_weather(self, city: str) -> dict:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        timeout = httpx.Timeout(5.0, connect=3.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.get(UPSTREAM_SERVICE_URL, params=params)
                response.raise_for_status()
                return response.json()
            
            except httpx.HTTPStatusError as e:
                status = e.response.status_code

                if status == 404:
                    raise CityNotFoundError(city)
                elif status == 401:
                    raise InvalidUpstreamApiKeyError()
                elif 500 <= status < 600:
                    raise UpstreamUnavailableError(f"Weather API returned {status}")
                else:
                    raise UpstreamBadResponseError(
                        f"Unexpected response {status}: {e.response.text[:200]}"
                    )

            except httpx.RequestError as e:
                raise UpstreamUnavailableError(f"Connection error: {str(e)}")