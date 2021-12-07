import sys,time, json, os
sys.path.insert(1,".")
from WeatherApps.currentWeather import currentWeather

def currentWeatherThread():
    try:
        while True:
            #Get Weather and save to json file
    
            with open(os.path.join('WeatherApps','tmp','currentWeather.json'),'w') as f:
                json.dump(currentWeather("Markham"),f)
      
            #wait 30 minutes
            time.sleep(1800)
    except KeyboardInterrupt:
        print("keyboard interrupt")
        sys.exit(0)