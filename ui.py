from tkinter import *
from PIL import Image, ImageTk
import weather_app
import datetime
import requests
from io import BytesIO

def refresh_data():
	new_data = weather_app.refresh()

	refresh_all_fields(new_data)

def refresh_all_fields(data):
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

def get_new_icon(url):
	img_data = requests.get(url).content
	img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
	return img

root = Tk()

root.title('Weather App')
root.geometry('400x300')
root.configure(bg="#F0F0F0")

city = Label(root, text="", bg="#F0F0F0")
description = Label(root, text="", bg="#F0F0F0")
first_icon = get_new_icon("https://openweathermap.org/img/wn/01d@2x.png")
weather_icon = Label(root, image=first_icon, bg="#F0F0F0")
temp = Label(root, text="", bg="#F0F0F0")
humidity = Label(root, text="", bg="#F0F0F0")
windsp = Label(root, text="", bg="#F0F0F0")
sunrise = Label(root, text="", bg="#F0F0F0")
sunset = Label(root, text="", bg="#F0F0F0")
timestamp = Label(root, text="", font=("Courier", 9), bg="#F0F0F0")

refresh_data()

city.pack()
description.pack()
weather_icon.pack()
temp.pack()
humidity.pack()
windsp.pack()
sunrise.pack()
sunset.pack()

refresh_btn = Button(root, text="Refresh", command=refresh_data, highlightbackground="#F0F0F0")
refresh_btn.pack()

timestamp.pack()


root.mainloop()