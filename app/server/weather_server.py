import grpc
from concurrent import futures
import asyncio

from generated import weather_pb2_grpc, weather_pb2
from app.services.weather_service import WeatherService
from app.adapters.weather_adapter import WeatherAdapter
from app.exceptions.weather_exceptions import (
    CityNotFoundError,
    InvalidUpstreamApiKeyError,
    UpstreamUnavailableError,
    WeatherValidationError,
    UpstreamBadResponseError,
)
from app.config import SERVER_PORT, API_KEY


class WeatherServicer(weather_pb2_grpc.WeatherServicer):

    def __init__(self, service: WeatherService):
        """
        Initializes the WeatherServicer with a WeatherService instance.

        Args:
            service (WeatherService): The service used to fetch and process weather data.
        """
        self.service = service
    
    async def GetWeatherInfo(self, request, context):
        """
        Handles incoming GetWeatherInfo gRPC requests.

        Validates the API key from metadata, checks the city name, fetches weather data,
        and returns a WeatherResponse message. Handles and maps various exceptions to
        appropriate gRPC status codes.

        Args:
            request: The WeatherRequest message containing the city name.
            context: The gRPC context for the request.

        Returns:
            WeatherResponse: The response message with weather data.
        """
        metadata = dict(context.invocation_metadata())
        client_key = metadata.get("x-api-key")

        if client_key != API_KEY:
            await context.abort(
                grpc.StatusCode.PERMISSION_DENIED,
                "Invalid or missing API key for gRPC access."
            )
        city =  request.city_name.strip()
        
        if not city:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "City name cannot be empty.")
        try:
            weather_data = await self.service.get_weather_data(city)
            return weather_pb2.WeatherResponse(
                city_name=weather_data['city_name'],
                temperature=weather_data['temperature'],
                weather_description=weather_data['weather_description'],
                humidity_percent=weather_data['humidity_percent'],
                wind_speed=weather_data['wind_speed']
            )
        except CityNotFoundError:
            await context.abort(grpc.StatusCode.NOT_FOUND, f"City '{city}' not found.")
        except InvalidUpstreamApiKeyError:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, "Invalid API key for upstream service.")
        except UpstreamUnavailableError:
            await context.abort(grpc.StatusCode.UNAVAILABLE, "Weather service is temporarily unavailable.")
        except UpstreamBadResponseError:
            await context.abort(grpc.StatusCode.INTERNAL, "Malformed response from weather provider.")
        except WeatherValidationError as e:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, f"Internal server error: {str(e)}") 
            
async def serve():
    adapter = WeatherAdapter()
    service = WeatherService(adapter)
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServicer_to_server(WeatherServicer(service), server)
    
    server.add_insecure_port(f'[::]:{SERVER_PORT}')
    print(f"Starting gRPC server on port {SERVER_PORT}...")
    await server.start()
    await server.wait_for_termination()
    
if __name__ == "__main__":
    asyncio.run(serve())
    