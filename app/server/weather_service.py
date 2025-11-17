from app.adapters.weather_adapter import WeatherAdapter
from pprint import pprint
from app.exceptions.weather_exceptions import (
    WeatherError,
    UpstreamBadResponseError,
)

class WeatherService:
    """
    Service class for processing and formatting weather data.

    This class uses a WeatherAdapter to fetch raw weather data from an external API,
    processes the data, and returns it in a structured dictionary format.
    """
    
    def __init__(self, adapter: WeatherAdapter):
        """
        Initializes the WeatherService with a given WeatherAdapter.

        Args:
            adapter (WeatherAdapter): The adapter used to fetch weather data.
        """
        self.adapter = adapter
        
    async def get_weather_data(self, city: str) -> dict:
        """
        Fetches and processes weather data for a given city.

        Args:
            city (str): The name of the city for which to retrieve weather data.

        Returns:
            dict: A dictionary containing processed weather data, including city name,
                  temperature, weather description, humidity percentage, and wind speed.

        Raises:
            WeatherError: For known weather-related errors.
            UpstreamBadResponseError: If the adapter returns invalid or unexpected data,
                                      or if an unexpected error occurs.
        """
        try:
            raw_weather_data = await self.adapter.get_weather(city)
            
            if not isinstance(raw_weather_data, dict):
                raise UpstreamBadResponseError("Adapter returned non-dict data")
            
            main = raw_weather_data.get("main", {})
            wind = raw_weather_data.get("wind", {})
            weather_list = raw_weather_data.get("weather", [])

            temperature = round(float(main.get("temp", 0.0)), 1)
            humidity = int(main.get("humidity", 0))
            wind_speed = round(float(wind.get("speed", 0.0)), 1)
            
            return {
                "city_name": raw_weather_data.get("name", city),
                "temperature": temperature,
                "weather_description": (
                    weather_list[0].get("description", "")
                    if weather_list and isinstance(weather_list[0], dict)
                    else ""
                ),
                "humidity_percent": humidity,
                "wind_speed": wind_speed,
            }
        except WeatherError:
            raise

        except (KeyError, TypeError, ValueError) as e:
            raise UpstreamBadResponseError(
                f"Invalid weather data format: {str(e)}"
            ) from e

        except Exception as e:
            raise UpstreamBadResponseError(f"Unexpected error in WeatherService: {e}") from e
    