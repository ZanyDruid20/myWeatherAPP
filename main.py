# main.py

import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

openweather_api_key = os.environ.get('OPENWEATHER_API_KEY')

if openweather_api_key is None:
    raise ValueError("No API key set for OpenWeather. Please set the OPENWEATHER_API_KEY environment variable.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    if not city:
        return render_template('index.html', error="City name is required ")
    weather_data = get_weather_data(city)
    forecast_data = get_forecast_data(city)
    if not weather_data:
        return render_template('result.html', weather_data=None)
    return render_template('result.html', weather_data=weather_data, forecast_data=forecast_data)

@app.route('/api/weather', methods=['GET'])
def api_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude parameters are required'}), 400
    weather_data = get_weather_data_by_coords(lat, lon)
    if not weather_data:
        return jsonify({'error': 'Weather data not found for the coordinates'}), 404
    return jsonify(weather_data)

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
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
        return None

def get_forecast_data(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={openweather_api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_list = data['list']
        forecast_data = []
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
        return None

def get_weather_data_by_coords(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweather_api_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
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
        return None

if __name__ == '__main__':
    print(f"OPENWEATHER_API_KEY: {os.environ.get('OPENWEATHER_API_KEY')}")
    app.run(debug=True)
