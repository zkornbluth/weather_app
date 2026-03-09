'''
Filename: main.py
Author: Zachary Kornbluth <github.com/zkornbluth>
Description: Generates Tkinter widget that displays weather data
'''

from tkinter import *
from PIL import Image, ImageTk
import weather_app
import requests
from io import BytesIO


def clear_display():
	city.configure(text="")
	description.configure(text="")
	weather_icon.configure(image=first_icon)
	weather_icon.image = first_icon
	temp.configure(text="")
	humidity.configure(text="")
	windsp.configure(text="")
	sunrise.configure(text="")
	sunset.configure(text="")
	timestamp.configure(text="")


def show_error(message):
	error_label.configure(text=message)
	clear_display()


def refresh_data():
	# Clear any previous error
	error_label.configure(text="")

	lat_str = lat_entry.get().strip()
	lon_str = lon_entry.get().strip()

	try:
		# If either latitude or longitude is provided, require and validate both
		if lat_str or lon_str:
			if not lat_str or not lon_str:
				raise ValueError("Both latitude and longitude are required.")

			lat = float(lat_str)
			lon = float(lon_str)

			if not (-90 <= lat <= 90):
				raise ValueError("Invalid latitude. Must be between -90 and 90.")
			if not (-180 <= lon <= 180):
				raise ValueError("Invalid longitude. Must be between -180 and 180.")

			new_data = weather_app.refresh(lat, lon, units=unit_var.get())
		else:
			new_data = weather_app.refresh(units=unit_var.get())

		refresh_all_fields(new_data)

	except ValueError as ve:
		# Handles invalid input ranges or API key/response errors from weather_app
		show_error(str(ve))
	except requests.exceptions.RequestException:
		show_error("Network error: Check your internet connection.")
	except Exception as e:
		# Catch-all for any other unexpected issues
		show_error(f"Unexpected error: {e}")

def refresh_all_fields(data): # Updates all labels with new data
	city.configure(text="Weather for {0}:".format(data['city']))
	description.configure(text=data['description'])
	icon = get_new_icon(data['icon_url'])
	weather_icon.configure(image=icon)
	weather_icon.image = icon
	temp.configure(text="{0}°{1}, feels like {2}°".format(data['temp'], data['temp_unit'], data['feelslike']))
	humidity.configure(text="Humidity: {0}%".format(data['humidity']))
	windsp.configure(text="Winds of {0} {1}".format(data['windsp'], data['wind_unit']))
	sunrise.configure(text="Sunrise: {0}".format(data['sunrise']))
	sunset.configure(text="Sunset: {0}".format(data['sunset']))
	timestamp.configure(text="Weather as of {0}".format(data['timestamp']))

def get_new_icon(url): # Retrieves new icon via the OpenWeather API
	try:
		result = requests.get(url, timeout=5)
		result.raise_for_status()
		img_data = result.content
	except requests.exceptions.RequestException:
		# Propagate to be handled in refresh_data
		raise

	img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
	return img

root = Tk()

root.title('Weather App')
root.geometry('400x480')
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
error_label = Label(root, text="", fg="red", bg="#E8E8E8", font=("Courier", 10))

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

# Unit toggle (imperial = °F, mph | metric = °C, km/h)
unit_var = StringVar(value="imperial")
unit_check = Checkbutton(
	root, text="Use metric units (Celsius, km/h)", variable=unit_var,
	onvalue="metric", offvalue="imperial", command=refresh_data,
	bg="#E8E8E8", font=("Courier", 10), selectcolor="#E8E8E8",
	activebackground="#E8E8E8"
)
unit_check.grid(row=7, column=0, columnspan=2, pady=(10, 0))

# Latitude and longitude labels and entries
lat_label = Label(root, text="Latitude:", bg="#E8E8E8", font=("Courier", 14))
lat_entry = Entry(root)
lon_label = Label(root, text="Longitude:", bg="#E8E8E8", font=("Courier", 14))
lon_entry = Entry(root)

# Grid for latitude and longitude labels and entries
lat_label.grid(row=8, column=0, sticky=E, pady=(10, 0))
lat_entry.grid(row=8, column=1, sticky=W, pady=(10, 0))
lon_label.grid(row=9, column=0, sticky=E)
lon_entry.grid(row=9, column=1, sticky=W)

# Refresh button
refresh_btn = Button(root, text="Refresh", command=refresh_data, highlightbackground="#E8E8E8")
refresh_btn.grid(row=10, column=0, columnspan=2)

# Timestamp
timestamp.grid(row=11, column=0, columnspan=2)

# Error message
error_label.grid(row=12, column=0, columnspan=2)

# Initial data refresh
refresh_data()

root.grid_columnconfigure((0, 1), weight=1)


root.mainloop()