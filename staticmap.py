import requests

    
url = "https://restapi.amap.com/v3/staticmap?"

parameters = {
    "key={}".format("fd337d528a81da2c3c1abdd237438560"),
    "location={}".format("116.405285,39.904989"),
    "zoom={}".format("15"), #[1,17]
    "size={}".format("720*720"),
    "scale={}".format("1"),
    "markers={}".format("mid,,A:116.405285,39.904989"),
    #"labels={}".format(""),
    #"paths={}".format(""),
    "traffic={}".format("0")
}

weather_url = url + '&'.join(parameters)

response = requests.get(url=weather_url)

if response.status_code == 200:
    with open("statics/images/map.jpg","wb") as file_obj:
        file_obj.write(response.content)
    
else:
    print("Status code: {}".format(response.status_code))