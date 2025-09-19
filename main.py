'''
Filename: main.py
Author: Zach Kornbluth
GitHub: github.com/zkornbluth
Description: Generates Tkinter widget that displays weather data
'''

from tkinter import *
from PIL import Image, ImageTk
import weather_app
import requests
from io import BytesIO

def refresh_data():
	# Get latitude and longitude from user input
	lat = lat_entry.get().strip()
	lon = lon_entry.get().strip()

	if lat and lon:
		new_data = weather_app.refresh(lat, lon)
	else:
		new_data = weather_app.refresh() # Refresh using latitude and longitude from latlong.py

	refresh_all_fields(new_data)

def refresh_all_fields(data): # Updates all labels with new data
	city.configure(text="Weather for {0}:".format(data['city']))
	description.configure(text=data['description'])
	icon = get_new_icon(data['icon_url'])
	weather_icon.configure(image=icon)
	weather_icon.image = icon
	temp.configure(text="{0}°F, feels like {1}°".format(data['temp'], data['feelslike']))
	humidity.configure(text="Humidity: {0}%".format(data['humidity']))
	windsp.configure(text="Winds of {0} mph".format(data['windsp']))
	sunrise.configure(text="Sunrise: {0}".format(data['sunrise']))
	sunset.configure(text="Sunset: {0}".format(data['sunset']))
	timestamp.configure(text="Weather as of {0}".format(data['timestamp']))

def get_new_icon(url): # Retrieves new icon via the OpenWeather API
	img_data = requests.get(url).content
	img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
	return img

root = Tk()

root.title('Weather App')
root.geometry('400x420')
root.configure(bg="#E8E8E8")

# Labels
city = Label(root, text="", bg="#E8E8E8", font=("Courier", 20))
description = Label(root, text="", bg="#E8E8E8", font=("Courier", 20))
first_icon = get_new_icon("https://openweathermap.org/img/wn/01d@2x.png")
weather_icon = Label(root, image=first_icon, bg="#E8E8E8")
temp = Label(root, text="", bg="#E8E8E8", font=("Courier", 20))
humidity = Label(root, text="", bg="#E8E8E8", font=("Courier", 20))
windsp = Label(root, text="", bg="#E8E8E8", font=("Courier", 20))
sunrise = Label(root, text="", bg="#E8E8E8", font=("Courier", 20))
sunset = Label(root, text="", bg="#E8E8E8", font=("Courier", 20))
timestamp = Label(root, text="", font=("Courier", 9), bg="#E8E8E8")

# Grid layout
# 2 columns to get weather_icon and description side by side
city.grid(pady=10, row=0, column=0, columnspan=2)
description.grid(row=1, column=0, sticky=E)
weather_icon.grid(row=1, column=1, sticky=W)
temp.grid(row=2, column=0, columnspan=2)
humidity.grid(row=3, column=0, columnspan=2)
windsp.grid(row=4, column=0, columnspan=2)
sunrise.grid(row=5, column=0, columnspan=2)
sunset.grid(row=6, column=0, columnspan=2)

# Latitude and longitude labels and entries
lat_label = Label(root, text="Latitude:", bg="#E8E8E8", font=("Courier", 14))
lat_entry = Entry(root)
lon_label = Label(root, text="Longitude:", bg="#E8E8E8", font=("Courier", 14))
lon_entry = Entry(root)

# Grid for latitude and longitude labels and entries
lat_label.grid(row=7, column=0, sticky=E, pady=(25, 0))
lat_entry.grid(row=7, column=1, sticky=W, pady=(25, 0))
lon_label.grid(row=8, column=0, sticky=E)
lon_entry.grid(row=8, column=1, sticky=W)

# Refresh button
refresh_btn = Button(root, text="Refresh", command=refresh_data, highlightbackground="#E8E8E8")
refresh_btn.grid(row=9, column=0, columnspan=2)

# Timestamp
timestamp.grid(row=10, column=0, columnspan=2)

# Initial data refresh
refresh_data()

root.grid_columnconfigure((0, 1), weight=1)


root.mainloop()