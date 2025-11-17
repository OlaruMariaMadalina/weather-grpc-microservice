class WeatherError(Exception):
    """Base class for all weather-related exceptions."""
    pass


class WeatherValidationError(WeatherError):
    """Raised when input (city name) is invalid or missing."""
    def __init__(self, city: str, message: str = "Invalid city name"):
        super().__init__(f"{message}: {city}")
        self.city = city


class CityNotFoundError(WeatherError):
    """Raised when the city is not found by the weather API."""
    def __init__(self, city: str):
        super().__init__(f"City not found: {city}")
        self.city = city


class InvalidUpstreamApiKeyError(WeatherError):
    """Raised when the OpenWeather API key is invalid or missing."""
    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(message)


class UpstreamUnavailableError(WeatherError):
    """Raised when the OpenWeather API is temporarily unavailable."""
    def __init__(self, message: str = "Weather service unavailable"):
        super().__init__(message)


class UpstreamBadResponseError(WeatherError):
    """Raised when OpenWeather returns malformed or unexpected data."""
    def __init__(self, message: str = "Invalid response from weather API"):
        super().__init__(message)
