import requests
from datetime import datetime
import os
from latlong import *

# Free API - but will want to hide this if we post online so we don't exceed free limits
OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']

# Call API
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}&units=imperial".format(lat, long, OPENWEATHER_API_KEY)

def refresh():
	return_obj = {}

	result = requests.get(WEATHER_API_URL)
	data = result.json()

	return_obj['city'] = data['name']
	return_obj['description'] = data['weather'][0]['main']
	icon = data['weather'][0]['icon']
	return_obj['icon_url'] = "https://openweathermap.org/img/wn/{0}@2x.png".format(icon)
	return_obj['temp'] = data['main']['temp']
	return_obj['feelslike'] = data['main']['feels_like']
	return_obj['humidity'] = data['main']['humidity']
	return_obj['windsp'] = data['wind']['speed']
	sunrise_utc = data['sys']['sunrise']
	return_obj['sunrise'] = datetime.fromtimestamp(sunrise_utc).strftime('%I:%M %p')
	sunset_utc = data['sys']['sunset']
	return_obj['sunset'] = datetime.fromtimestamp(sunset_utc).strftime('%I:%M %p')
	return_obj['timestamp'] = datetime.fromtimestamp(data['dt']).strftime("%m/%d/%Y, %I:%M:%S %p")

	return return_obj

# OLD - process and print in this doc

# result = requests.get(WEATHER_API_URL)
# data = result.json()

# # Display weather for that location
# city = data["name"]
# description = data["weather"][0]["main"]
# icon = data["weather"][0]["icon"]
# icon_url = "https://openweathermap.org/img/wn/{0}@2x.png".format(icon)
# temp = data["main"]["temp"]
# feelslike = data["main"]["feels_like"]
# humidity = data["main"]["humidity"]
# windsp = data["wind"]["speed"]
# sunrise_utc = data["sys"]["sunrise"]
# sunrise = datetime.fromtimestamp(sunrise_utc).strftime('%I:%M %p')
# sunset_utc = data["sys"]["sunset"]
# sunset = datetime.fromtimestamp(sunset_utc).strftime('%I:%M %p')

# print("")
# print("Weather in {0}:".format(city))
# print(description)
# print("{0}°F, feels like {1}°".format(temp, feelslike))
# print("Humidity: {0}%".format(humidity))
# print("Winds of {0} mph".format(windsp))
# print("Sunrise: {0}".format(sunrise))
# print("Sunset: {0}".format(sunset))
# print("")

