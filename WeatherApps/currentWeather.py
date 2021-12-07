import requests,sys
import requests
sys.path.insert(1,".")
from config import OPEN_WEATHER_API_KEY
#Rate Limit: 1 per second (1 000 000 per minute/2 per second).
toCelsius = lambda x: x - 272.15
fix = lambda x: round(x,2)
#This function gets all the tasks in the "Tasks" project which is the the project to be used.
def currentWeather(city):
    #Get all the tasks in project and turn it into a list of dicts.
    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_API_KEY}').json()    #Weather Get: main/decription, icon?, windspeed, temp/feelslike, temp min/max

    #Filter out all the useless data
    temp = {
        "Summary": weather["weather"][0]["main"],
        "Icon":weather["weather"][0]["icon"],
        "Temp": fix(toCelsius(weather["main"]["temp"])),
        "Feels Like": fix(toCelsius(weather["main"]["feels_like"])),
        "Wind Speed": fix(weather["wind"]["speed"]  * 3.6),
        "Temp Min": fix(weather["main"]["temp_min"]),
        "Temp Max": fix(weather["main"]["temp_max"]),
    }

    return temp