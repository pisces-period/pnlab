# import statements
import pyowm
import os

# get environment variables from the CLI
API_KEY=os.environ.get('OPENWEATHER_API_KEY')
CITY_NAME=os.environ.get('CITY_NAME')

if __name__=='__main__':
    try:
        # get a OWM Object based on API key
        weather_man=pyowm.OWM(API_key=API_KEY)
        
    except:
        # print error and quit
        print("invalid API key. Please check your API key and try again")
        exit(0)
        
    try:
        # invokes API call to 'api.openweathermap.org/data/2.5/weather?q=${CITY_NAME} - returns an observation object
        obs=weather_man.weather_at_place(CITY_NAME)
    except:
        # print error and quit
        print("invalid city. Please check the city name and try again")
        exit(0)
    
    # API calls might timeout from time to time based on network latency
    # adding try/except block to handle timeouts
    
    try:
        # get weather object
        weather=obs.get_weather()
    except:
        # print error and quit
        print("unable to get weather data. Please try again later")
        exit(0)

    try:
        # get location object
        location=obs.get_location()
    except:
        # print error and quit
        print("unable to get location data. Please try again later")
    
    # Print to STDOUT
    print("{}:{},{}:{},{}:{},{}:{},{}:{}".format(
                                                    "source","openweathermap","location",location.get_name(),
                                                    "description", weather.get_detailed_status(),"temp",weather.get_temperature(unit='celsius').get("temp"),
                                                    "humidity",weather.get_humidity())
                                                    
                                                    )