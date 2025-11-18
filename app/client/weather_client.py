import grpc
from generated import weather_pb2_grpc, weather_pb2
import asyncio
from app.config import SERVER_ADDR, API_KEY, SERVER_TIMEOUT, SERVER_PORT

async def main():
    """
    Runs the asynchronous gRPC weather client.

    Connects to the weather gRPC server, prompts the user for city names,
    sends requests to the server, and displays formatted weather information.
    Handles and displays errors for unavailable server, timeouts, and other gRPC errors.
    """
    async with grpc.aio.insecure_channel(f"{SERVER_ADDR}:{SERVER_PORT}") as channel:
        stub = weather_pb2_grpc.WeatherStub(channel)
        
        while True:
            city = input("\nEnter the city you want to check the weather for (or type 'exit' to quit): ")
            
            try:
                metadata = [("x-api-key", API_KEY)]
                
                response = await stub.GetWeatherInfo(
                    weather_pb2.WeatherRequest(city_name=city),
                    metadata=metadata,
                    timeout=SERVER_TIMEOUT,
                )
                print(f"\nWeather for {response.city_name}:")
                print(f"Temperature: {response.temperature} °C")
                print(f"Humidity: {response.humidity_percent}%")
                print(f"Conditions: {response.weather_description}")
                print(f"Wind Speed: {response.wind_speed} m/s")
            
            except grpc.aio.AioRpcError as e:
                code = e.code()
                message = e.details() or ""
                if code == grpc.StatusCode.UNAVAILABLE:
                    print("[ERROR] Server is not available. Please try again later.")
                elif code == grpc.StatusCode.DEADLINE_EXCEEDED:
                    print("[ERROR] Server took too long to respond. Please try again later.")
                else:
                    print(f"[ERROR] {code.name}: {message}")
                
if __name__ == "__main__":
    asyncio.run(main())              
    