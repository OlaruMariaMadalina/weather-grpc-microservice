# WeatherApp

## How to Run the Application

### 1. Clone the repository and install dependencies

```bash
git clone <repository-url>
cd WeatherApp
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set environment variables

Create a `.env` file in the project root with the following content:

```
OPEN_WEATHER_API_KEY=your_openweathermap_api_key
API_KEY=your_custom_api_key
SERVER_PORT=50051
SERVER_ADDR=localhost
SERVER_TIMEOUT=5.0
UPSTREAM_SERVICE_URL=http://api.openweathermap.org/data/2.5/weather
```

### 3. Generate gRPC code from proto file

```bash
python -m grpc_tools.protoc -I./proto --python_out=./generated --grpc_python_out=./generated ./proto/weather.proto
```

### 4. Run the gRPC server

```bash
py -m app.server.weather_server
```

### 5. Run the gRPC client (in a new terminal)

```bash
py -m app.client.weather_client
```