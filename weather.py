import requests
import json
from django.http import HttpResponse
from django.shortcuts import render
weather_url = "	https://restapi.amap.com/v3/weather/weatherInfo?"
citycode_url="https://restapi.amap.com/v3/geocode/regeo?"
position_parameters = {
    "key={}".format("fd337d528a81da2c3c1abdd237438560"),

    "location={}".format("115.04358735887,37.227088328938"),

    "extensions={}".format("base"), #base:实况天气 all:预报天气

    "output={}".format("JSON") #JSON XML
}
citycode_url = citycode_url + '&'.join(position_parameters)
response = requests.get(url=citycode_url)
js1 = json.dumps(response.json(),ensure_ascii=False,indent=4)

weather_position_info={}

t = js1.find('adcode')
js = js1[t:]
t1 = js.find(":")
t2 = js.find(',')
city_code=js[t1+3:t2-1]
weather_position_info["adcode"]=city_code

t = js1.find('formatted_address')
js = js1[t:]
print(js)
t1 = js.find(':')
js=js[t1+3:]
t2 = js.find('"')
weather_position_info["address"]=js[:t2]

weather_parameters = {
    "key={}".format("fd337d528a81da2c3c1abdd237438560"),

    "city={}".format(city_code),

    "extensions={}".format("base"), #base:实况天气 all:预报天气

    "output={}".format("JSON") #JSON XML
}

weather_url = weather_url + '&'.join(weather_parameters)

response = requests.get(url=weather_url)

js1 = json.dumps(response.json(),ensure_ascii=False,indent=4)

t = js1.find('province')
js = js1[t:]
t1 = js.find(":")
t2 = js.find(',')
weather_position_info['province'] = js[t1+3:t2-1]
#print(js[t1+3:t2-1])
t = js.find('city')
js = js[t:]
t1 = js.find(":")
t2 = js.find(',')
weather_position_info['city'] = js[t1 + 3:t2 - 1]
#print(js[t1 + 3:t2 - 1])
t = js.find('weather')
js = js[t:]
t1 = js.find(":")
t2 = js.find(',')
weather_position_info['weather'] = js[t1 + 3:t2 - 1]
#print(js[t1 + 3:t2 - 1])
t = js.find('temperature')
js = js[t:]
t1 = js.find(":")
t2 = js.find(',')
weather_position_info['temperature'] = js[t1 + 3:t2 - 1]
#print(js[t1 + 3:t2 - 1])
t = js.find('winddirection')
js = js[t:]
t1 = js.find(":")
t2 = js.find(',')
#print(t,t1,t2)
weather_position_info['winddirection'] = js[t1 + 3:t2 - 1]
t = js.find('windpower')
js = js[t:]
t1 = js.find(":")
t2 = js.find(',')
weather_position_info['windpower'] = js[t1 + 3:t2 - 1]
t = js.find('humidity')
js = js[t:]
t1 = js.find(":")
t2 = js.find(',')
#print(t,t1, t2)
weather_position_info['humidity'] = js[t1 + 3:t2 - 1]

    




