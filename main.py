import os
import requests
from flask import Flask, render_template, request, jsonify

# Create an instance of the Flask class
app = Flask(__name__)

# Get the OpenWeather API key from environment variables
openweather_api_key = os.environ.get('OPENWEATHER_API_KEY')

# Check if the API key is set; if not, raise an error
if openweather_api_key is None:
    raise ValueError("No API key set for OpenWeather. Please set the OPENWEATHER_API_KEY environment variable.")

# Define the route for the home page
@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

# Define the route for the weather form submission
@app.route('/weather', methods=['POST'])
def weather():
    # Get the city name from the form
    city = request.form['city']
    if not city:
        # If no city is provided, return to the index page with an error message
        return render_template('index.html', error="City name is required ")
    # Get the current weather data for the city
    weather_data = get_weather_data(city)
    # Get the forecast data for the city
    forecast_data = get_forecast_data(city)
    if not weather_data:
        # If weather data is not found, render the result page with no data
        return render_template('result.html', weather_data=None)
    # Render the result page with the weather and forecast data
    return render_template('result.html', weather_data=weather_data, forecast_data=forecast_data)

# Define the route for the API weather data retrieval
@app.route('/api/weather', methods=['GET'])
def api_weather():
    # Get the latitude and longitude from the query parameters
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        # If latitude or longitude is not provided, return an error response
        return jsonify({'error': 'Latitude and longitude parameters are required'}), 400
    # Get the weather data based on coordinates
    weather_data = get_weather_data_by_coords(lat, lon)
    if not weather_data:
        # If weather data is not found, return a not found response
        return jsonify({'error': 'Weather data not found for the coordinates'}), 404
    # Return the weather data as JSON
    return jsonify(weather_data)

# Function to get current weather data for a city
def get_weather_data(city):
    # Build the API URL for current weather data
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}&units=metric'
    # Send a request to the API
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract relevant weather information
        weather = {
            'description': data['weather'][0]['description'],
            'temperature': data['main']['temp'],
            'city': data['name'],
            'country': data['sys']['country'],
            'wind_speed': data['wind']['speed'],
            'humidity': data['main']['humidity']
        }
        return weather
    else:
        # Return None if the request was not successful
        return None

# Function to get weather forecast data for a city
def get_forecast_data(city):
    # Build the API URL for weather forecast data
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={openweather_api_key}&units=metric'
    # Send a request to the API
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        forecast_list = data['list']
        forecast_data = []
        # Extract relevant forecast information for each entry
        for entry in forecast_list:
            forecast = {
                'datetime': entry['dt_txt'],
                'description': entry['weather'][0]['description'],
                'temperature': entry['main']['temp'],
                'city': data['city']['name'],
                'country': data['city']['country']
            }
            forecast_data.append(forecast)
        return forecast_data
    else:
        # Return None if the request was not successful
        return None

# Function to get current weather data based on coordinates
def get_weather_data_by_coords(lat, lon):
    # Build the API URL for current weather data using coordinates
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweather_api_key}&units=metric'
    # Send a request to the API
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract relevant weather information
        weather = {
            'description': data['weather'][0]['description'],
            'temperature': data['main']['temp'],
            'city': data['name'],
            'country': data['sys']['country'],
            'wind_speed': data['wind']['speed'],
            'humidity': data['main']['humidity']
        }
        return weather
    else:
        # Return None if the request was not successful
        return None

# Entry point of the script
if __name__ == '__main__':
    # Print the API key to verify it is set (for debugging purposes)
    print(f"OPENWEATHER_API_KEY: {os.environ.get('OPENWEATHER_API_KEY')}")
    # Run the Flask application in debug mode
    app.run(debug=True)
