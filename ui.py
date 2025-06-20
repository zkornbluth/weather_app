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
	city.configure(text="Weather for {0}:".format(data['city']), bg="#EEEEEE")
	description.configure(text=data['description'], bg="#EEEEEE")
	icon = get_new_icon(data['icon_url'])
	print(data['icon_url'])
	weather_icon.configure(image=icon, bg="#EEEEEE")
	temp.configure(text="{0}°F, feels like {1}°".format(data['temp'], data['feelslike']), bg="#EEEEEE")
	humidity.configure(text="Humidity: {0}%".format(data['humidity']), bg="#EEEEEE")
	windsp.configure(text="Winds of {0} mph".format(data['windsp']), bg="#EEEEEE")
	sunrise.configure(text="Sunrise: {0}".format(data['sunrise']), bg="#EEEEEE")
	sunset.configure(text="Sunset: {0}".format(data['sunset']), bg="#EEEEEE")
	timestamp.configure(text="Last updated at {0}".format(datetime.datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")), bg="#EEEEEE")

def get_new_icon(url):
	img_data = requests.get(url).content
	img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
	return img

root = Tk()

root.title('Weather App')
root.geometry('400x300')
root.configure(bg="#EEEEEE")

city = Label(root, text="")
description = Label(root, text="")
weather_icon = Label(root, image=None)
temp = Label(root, text="")
humidity = Label(root, text="")
windsp = Label(root, text="")
sunrise = Label(root, text="")
sunset = Label(root, text="")
timestamp = Label(root, text="", font=("Courier", 9))

refresh_data()

city.pack()
description.pack()
weather_icon.pack()
temp.pack()
humidity.pack()
windsp.pack()
sunrise.pack()
sunset.pack()

refresh_btn = Button(root, text="Refresh", command=refresh_data, highlightbackground="#EEEEEE")
refresh_btn.pack()

timestamp.pack()


root.mainloop()