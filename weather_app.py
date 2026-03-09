'''
Filename: weather_app.py
Author: Zachary Kornbluth <github.com/zkornbluth>
Description: Fetches weather data from OpenWeather API
'''

import requests
from datetime import datetime, timedelta
import os
from urllib.parse import quote
from latlong import *


def _get_api_key():
	api_key = os.environ.get('OPENWEATHER_API_KEY')
	if not api_key:
		raise ValueError("API key error: Set OPENWEATHER_API_KEY environment variable.")
	return api_key


def geocode(city_name, api_key=None):
	"""
	Convert city name to lat/lon via OpenWeather Geocoding API.
	city_name can be "New York", "Springfield, MA", "London, UK", etc.
	Returns (lat, lon). Raises ValueError if no results or API error.
	"""
	if api_key is None:
		api_key = _get_api_key()
	url = "http://api.openweathermap.org/geo/1.0/direct?q={0}&limit=1&appid={1}".format(quote(city_name.strip()), api_key)
	try:
		result = requests.get(url, timeout=5)
		result.raise_for_status()
		results = result.json()
	except requests.exceptions.HTTPError as e:
		if result.status_code == 401:
			raise ValueError("API error: Check your OpenWeather API key.") from e
		raise ValueError("Geocoding API error. Try a different city name.") from e
	except requests.exceptions.RequestException:
		raise
	if not results:
		raise ValueError("No location found for that city.")
	first = results[0]
	return (first['lat'], first['lon'])


def refresh(lat=None, long=None, units='imperial'):
	return_obj = {}

	api_key = _get_api_key()
	units_param = 'metric' if units == 'metric' else 'imperial'

	if lat is not None and long is not None:
		weather_api_url = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}&units={3}".format(lat, long, api_key, units_param)
	else:
		weather_api_url = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}&units={3}".format(LAT, LONG, api_key, units_param)

	try:
		result = requests.get(weather_api_url, timeout=5)
		result.raise_for_status()
		data = result.json()
	except requests.exceptions.HTTPError as e:
		if result.status_code == 401:
			raise ValueError("API error: Check your OpenWeather API key.") from e
		else:
			raise ValueError(f"API error: HTTP {result.status_code} from weather service.") from e
	except requests.exceptions.RequestException:
		# Network-related error, let caller handle it
		raise
	except ValueError as e:
		# JSON decode error or similar
		raise ValueError("Invalid response from weather service.") from e

	# build return_obj for main.py
	# Weather data
	return_obj['city'] = data['name']
	return_obj['description'] = data['weather'][0]['main']
	icon = data['weather'][0]['icon']
	return_obj['icon_url'] = "https://openweathermap.org/img/wn/{0}@2x.png".format(icon)
	return_obj['temp'] = round(data['main']['temp'])
	return_obj['feelslike'] = round(data['main']['feels_like'])
	return_obj['humidity'] = data['main']['humidity']

	# OpenWeather: imperial = mph, metric = m/s. Convert m/s to km/h for metric.
	wind_raw = data['wind']['speed']
	if units_param == 'metric':
		return_obj['windsp'] = round(wind_raw * 3.6, 1)  # m/s -> km/h
		return_obj['wind_unit'] = 'km/h'
		return_obj['temp_unit'] = 'C'
	else:
		return_obj['windsp'] = wind_raw
		return_obj['wind_unit'] = 'mph'
		return_obj['temp_unit'] = 'F'

	# Use API timezone offset (seconds from UTC) for location-accurate times
	tz_offset_seconds = data.get('timezone', 0)
	tz_delta = timedelta(seconds=tz_offset_seconds)

	def utc_to_local(utc_timestamp):
		utc_time = datetime.utcfromtimestamp(utc_timestamp)
		return utc_time + tz_delta

	# Sunrise and sunset (UNIX timestamps in UTC)
	sunrise_local = utc_to_local(data['sys']['sunrise'])
	return_obj['sunrise'] = sunrise_local.strftime('%I:%M %p')
	sunset_local = utc_to_local(data['sys']['sunset'])
	return_obj['sunset'] = sunset_local.strftime('%I:%M %p')

	# Report timestamp
	dt_local = utc_to_local(data['dt'])
	return_obj['timestamp'] = dt_local.strftime("%m/%d/%Y, %I:%M:%S %p")

	return return_obj
