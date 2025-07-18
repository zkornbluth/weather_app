# Tkinter Weather Widget

## Project Description/Features
<img width="512" height="490" alt="weather-widget-2" src="https://github.com/user-attachments/assets/2ec13ea0-c831-4a79-91ec-3d472e8c2381" />

## Getting Started

Follow these simple steps to set up the widget on your local machine.

### 1. Clone the repository

```bash
git clone https://github.com/zkornbluth/weather_app.git
cd weather_app
```

### 2. Install Python packages
Make sure you have Python 3.9+ installed, then run:

```bash
pip install -r requirements.txt
```

### 3. Set up an OpenWeather API key
Go to OpenWeather's [website](https://openweathermap.org/). Create a free account and generate an API key. 

You can either copy and paste that into `weather_app.py` or save it as an environment variable by following the instructions [here](https://www.alibabacloud.com/help/en/model-studio/configure-api-key-through-environment-variables). If you do save it as an environment variable, be sure to name it `OPENWEATHER_API_KEY` as that's what `weather_app.py` is looking for.

### 4. Set your location

Update the `lat` and `long` variables in `latlong.py` to the latitude and longitude for your desired location. Use positive values for North and East and negative values for South and West.

### 5. Run the app

```bash
python3 main.py
```
