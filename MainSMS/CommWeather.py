import pytextnow as pytn
import requests, json
import time
import math
import Credentials
username = Credentials.username()
sid = Credentials.sid()
csrf = Credentials.csrf()
client = pytn.Client(username, sid_cookie=sid, csrf_cookie=csrf)
def weathercheck(msg):
    resp = ""
    city_name = "chicago"
    state_code = "il"
    country_code = "us"
    api_key = Credentials.WeatherKey()
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    resp = ask("Enter city name:", msg)
    if resp != "" and resp is not None:
        city_name = resp
    resp = ask("Enter two letter state abbreviation:", msg)
    if resp != "" and resp is not None:
        state_code = resp
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "," + state_code + "," + country_code
    print(complete_url)
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404" and x["cod"] != "400":
        y = x["main"]
        current_temperature = (y["temp"]*1.8 - 459.67)
        current_temperature = math.floor(current_temperature)
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"] 
        msg.send_sms("weather in " + str(city_name) + ":")
        time.sleep(1)
        msg.send_sms(str(weather_description))
        time.sleep(1)
        msg.send_sms("Temperature: " + str(current_temperature) + "\u00B0\u0046")
        msg.send_sms("Air Pressure: " + str(current_pressure) +"hpa")
        msg.send_sms("Humidity: " + str(current_humidity) + "%")
    else:
        error1 = "invalid city. please send Weather command again to retry."
        msg.send_sms(error1)
def ask(question, msg):
    timeout = time.perf_counter()
    exitloop = 0
##    time.sleep(1)
    msg.send_sms(question)
    resp = ""
    while time.perf_counter() - timeout <= 60 and exitloop != 1:
        new_messages = client.get_unread_messages()
        exitloop = 0
        for message in new_messages:
            if message.number == msg.number:
                message.mark_as_read()
                return message.content #left off working here
