'''
Filename: weather_app.py
Author: Zachary Kornbluth <github.com/zkornbluth>
Description: Fetches weather data from OpenWeather API
'''

import requests
from datetime import datetime
import os
from latlong import *

# Free API, instructions in README to set up
OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']

def refresh(lat=None, long=None):
	return_obj = {}

	if lat and long:
		weather_api_url = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}&units=imperial".format(lat, long, OPENWEATHER_API_KEY)	
	else:
		weather_api_url = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}&units=imperial".format(LAT, LONG, OPENWEATHER_API_KEY)

	result = requests.get(weather_api_url)
	data = result.json()

	# build return_obj for main.py
	# Weather data
	return_obj['city'] = data['name']
	return_obj['description'] = data['weather'][0]['main']
	icon = data['weather'][0]['icon']
	return_obj['icon_url'] = "https://openweathermap.org/img/wn/{0}@2x.png".format(icon)
	return_obj['temp'] = round(data['main']['temp'])
	return_obj['feelslike'] = round(data['main']['feels_like'])
	return_obj['humidity'] = data['main']['humidity']
	return_obj['windsp'] = data['wind']['speed']

	# Sunrise and sunset
	# Times come in as UTC, have to convert them
	sunrise_utc = data['sys']['sunrise']
	return_obj['sunrise'] = datetime.fromtimestamp(sunrise_utc).strftime('%I:%M %p')
	sunset_utc = data['sys']['sunset']
	return_obj['sunset'] = datetime.fromtimestamp(sunset_utc).strftime('%I:%M %p')

	# Timestamp
	return_obj['timestamp'] = datetime.fromtimestamp(data['dt']).strftime("%m/%d/%Y, %I:%M:%S %p")

	return return_obj
