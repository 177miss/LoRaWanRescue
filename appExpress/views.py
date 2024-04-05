from django.http import HttpResponse
from django.shortcuts import render
from appExpress.models import users,Message,Gateway,Client
from django.http import JsonResponse
from django.core.serializers import serialize
from django.shortcuts import redirect
from geopy.geocoders import Nominatim

def get_city_from_coordinates(latitude, longitude):
    key = "fd337d528a81da2c3c1abdd237438560"
    url = f"https://restapi.amap.com/v3/geocode/regeo?key={key}&location={longitude},{latitude}&extensions=base"
    response = requests.get(url)
    data = response.json()
    city = data['regeocode']['addressComponent']['city']
    if (type(city) == list):
        if (len(city) == 0):
            return None
        else:
            return city[0]
    return city

def city_rank():
    ans = {}
    mes = Message.objects.all()
    for m in mes:
        l,r = m.latitude,m.longitude
        city = get_city_from_coordinates(l,r)
        ans[city] = ans.get(city,0)+1
    ans = dict(sorted(ans.items(), key=lambda item: item[1], reverse=True))
    if (len(ans)<10):
        return ans
    else:
        top_10 = dict(list(ans.items())[:10])
        return top_10

def login(request):
    return render(request,'login.html',None)

def index(request):
    if request.method=='POST':
        login_dict={"id":"","pwd":""}
        login_dict["id"]=request.POST.get("id")
        login_dict["pwd"]=request.POST.get("pwd")
        user=users.objects.filter(id_admin=login_dict["id"],pwd_admin=login_dict["pwd"])
        if user:
            user = users.objects.all()
            message = Message.objects.all()
            gateway = Gateway.objects.all()
            client = Client.objects.all()
            num_client = len(client)
            num_gateway = len(gateway)
            num_message = len(message)
            num_sos = 0
            for mes in message:
                if "sos" in mes.Text or "SOS" in mes.Text:
                    num_sos+=1
            ans = {}
            ans['num_client'] = num_client
            ans['num_gateway'] = num_gateway
            ans['num_message'] = num_message
            ans['num_sos'] = num_sos
            return render(request,'index.html',{"user":user,"message":message,"gateway":gateway,"ans":ans})
        else:
            return render(request,'login.html',{"login_dict":login_dict})

def show_message(request):
    table_Message = Message.objects.filter(id__icontains=-1)
    for item in Message.objects.all():
        if (not table_Message.filter(Eui__icontains=item.Eui, Client__icontains=item.Client).exists()):
            table_Message_list = list(table_Message.all())
            table_Message_list.append(item)
            table_Message = Message.objects.filter(pk__in=[m.pk for m in table_Message_list])
    if request.method=='POST':
        opt_key=request.POST.get("opt-srch")
        opt_value=request.POST.get("opt")
        if(opt_value==''):
            return render(request, 'show_message.html', {"table_Message": table_Message})
        elif opt_key=="IP":
            table_Message = table_Message.filter(Client__icontains=opt_value)
        elif opt_key=="Time":
            table_Message = table_Message.filter(Time__icontains=opt_value)
        else:
            table_Message = table_Message.filter(Text__icontains=opt_value)
        table_Message=table_Message.order_by('-id')
        return render(request,'show_message.html',{"table_Message":table_Message})
    table_Message=table_Message.order_by('-id')
    return render(request,'show_message.html',{"table_Message":table_Message})

def show_users(request):
    table_client = Client.objects.all()
    return render(request,'show_users.html',{"table_client":table_client})

def show_map(request):
    table_client = Client.objects.all()
    
    return render(request,'show_map.html',{"table_client":table_client})


import requests
import json
def get_weather_info(request):
    latitude=str(request.POST.get("x"))
    longitude=str(request.POST.get("y"))
    weather_url = "	https://restapi.amap.com/v3/weather/weatherInfo?"
    citycode_url="https://restapi.amap.com/v3/geocode/regeo?"
    position_parameters = {
        "key={}".format("fd337d528a81da2c3c1abdd237438560"),

        "location={}".format("%s,%s"%(longitude,latitude)),

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
    weather_position_info['x'] = latitude
    weather_position_info['y'] = longitude
    return weather_position_info

def map_api(request):
    latitude=str(request.GET.get("x"))
    longitude=str(request.GET.get("y"))

    url = "https://restapi.amap.com/v3/staticmap?"

    parameters = {
        "key={}".format("fd337d528a81da2c3c1abdd237438560"),
        "location={}".format("%s,%s"%(longitude,latitude)),
        "zoom={}".format("15"), #[1,17]
        "size={}".format("720*720"),
        "scale={}".format("1"),
        "markers={}".format("mid,,A:%s,%s"%(longitude,latitude)),
        #"labels={}".format(""),
        #"paths={}".format(""),
        "traffic={}".format("0")
    }

    position_image_url = url + '&'.join(parameters)

    response = requests.get(url=position_image_url)

    if response.status_code == 200:
        with open("statics/images/map.jpg","wb") as file_obj:
            file_obj.write(response.content)
    else:
        print("Status code: {}".format(response.status_code))

    weather_url = "	https://restapi.amap.com/v3/weather/weatherInfo?"
    citycode_url="https://restapi.amap.com/v3/geocode/regeo?"
    position_parameters = {
        "key={}".format("fd337d528a81da2c3c1abdd237438560"),

        "location={}".format("%s,%s"%(longitude,latitude)),

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
    weather_position_info['x'] = latitude
    weather_position_info['y'] = longitude
    #position_image(request)
    weather_position_info = json.dumps(weather_position_info)

    

    return JsonResponse(weather_position_info,safe=False)


def position_image(request):

    latitude=str(request.POST.get("x"))
    longitude=str(request.POST.get("y"))
    url = "https://restapi.amap.com/v3/staticmap?"

    parameters = {
        "key={}".format("fd337d528a81da2c3c1abdd237438560"),
        "location={}".format("%s,%s"%(longitude,latitude)),
        "zoom={}".format("15"), #[1,17]
        "size={}".format("720*720"),
        "scale={}".format("1"),
        "markers={}".format("mid,,A:%s,%s"%(longitude,latitude)),
        #"labels={}".format(""),
        #"paths={}".format(""),
        "traffic={}".format("0")
    }

    position_image_url = url + '&'.join(parameters)

    response = requests.get(url=position_image_url)

    if response.status_code == 200:
        with open("statics/images/map.jpg","wb") as file_obj:
            file_obj.write(response.content)
    else:
        print("Status code: {}".format(response.status_code))

def position(request):
    weather_info=get_weather_info(request)
    position_image(request)
    return render(request,'position.html',weather_info)

def gateway(request):
    client = request.POST['Client']
    eui = request.POST['Eui']
    gateway = []
    for item in Message.objects.all():
        if (item.Client == client and eui == item.Eui):
            t = Gateway.objects.filter(G_id = item.Gateway)
            if (Gateway.objects.filter(G_id = item.Gateway).exists()):
                gateway.append(t[0])
    return render(request, 'show_gateway.html', {"gateway":gateway , "client":client,"eui":eui})

def situation_map(request):
    client = Client.objects.all()
    gateway = Gateway.objects.all()
    message = Message.objects.all()
    num_client = len(client)
    num_gateway = len(gateway)
    num_message = len(message)
    num_sos = 0
    for mes in message:
        if "sos" in mes.Text or "SOS" in mes.Text:
            num_sos+=1
    ans = {}
    ans['num_client'] = num_client
    ans['num_gateway'] = num_gateway
    ans['num_message'] = num_message
    ans['num_sos'] = num_sos
    return render(request, 'show_situation_map.html', {"ans":ans})

def management(request):
    user = users.objects.all()
    client = Client.objects.all()
    message = Message.objects.all()
    message = message.order_by("-id")
    gateway = Gateway.objects.all()
    num_client = len(client)
    num_gateway = len(gateway)
    num_message = len(message)
    num_sos = 0
    for mes in message:
        if "sos" in mes.Text or "SOS" in mes.Text:
                num_sos+=1
    ans = {}
    ans['num_client'] = num_client
    ans['num_gateway'] = num_gateway
    ans['num_message'] = num_message
    ans['num_sos'] = num_sos
    return render(request,'show_management.html',{"user":user,"client":client,"message":message,"gateway":gateway,"ans":ans})

def log(request):
    log = open("logs\server.log","r")
    content = log.readlines()
    l = len(content)
    ans = []
    for i in range(2,l):
        if ("2023" in content[i]):
            info = {}
            info['time'] = content[i][:23]
            object = content[i][23:].split()
            info['type'] = object[0][1:-1]
            t = ""
            for j in range(1,len(object)):
                t= t + " " + object[j]
            info['text'] = t
            ans.append(info)
        else:
            continue
    log.close()
    return render(request, 'show_log.html', {"table_log":ans})

def user_api(request):
    user_object = users.objects.all()
    user_json = serialize('json', user_object)
    return JsonResponse(user_json,safe=False)

def message_api(request):
    message_object = Message.objects.all()
    message_json = serialize('json', message_object)
    return JsonResponse(message_json,safe=False)

def gateway_api(request):
    gateway_object = Gateway.objects.all()
    gateway_json = serialize('json', gateway_object)
    return JsonResponse(gateway_json,safe=False)

def client_api(request):
    client_object = Client.objects.all()
    client_json = serialize('json',client_object)
    return JsonResponse(client_json,safe=False)

def test(request):
    user = users.objects.all()
    message = Message.objects.all()
    gateway = Gateway.objects.all()
    return render(request,'test.html',{"user":user,"message":message,"gateway":gateway})

def weather_api(request):
    latitude=str(request.GET.get("x"))
    longitude=str(request.GET.get("y"))
    weather_url = "	https://restapi.amap.com/v3/weather/weatherInfo?"
    citycode_url="https://restapi.amap.com/v3/geocode/regeo?"
    position_parameters = {
        "key={}".format("fd337d528a81da2c3c1abdd237438560"),

        "location={}".format("%s,%s"%(longitude,latitude)),

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
    weather_position_info['x'] = latitude
    weather_position_info['y'] = longitude
    info_json = json.dumps(weather_position_info)
    return JsonResponse(info_json,safe=False)

def handle_log(request):
    log = open("..\logs\server.log","r")
    content = log.readlines()
    l = len(content)
    ans = []
    for i in range(2,l):
        if ("2023" in content[i]):
            info["time"] = content[i][:23]
            object = content[i][23:].split()
            info = {}
            info['type'] = object[0][1:-1]
            t = ""
            for j in range(1,len(object)):
                t= t + " " + object[j]
            info['text'] = t
            ans.append(info)
        else:
            continue
    log.close()
    log_json = json.dumps(ans)
    return JsonResponse(log_json,safe=False)

def num_api(reuqest):
    client = Client.objects.all()
    gateway = Gateway.objects.all()
    message = Message.objects.all()
    num_client = len(client)
    num_gateway = len(gateway)
    num_message = len(message)
    num_sos = 0
    for mes in message:
        if "sos" in mes.Text or "SOS" in mes.Text:
            num_sos+=1
    ans = {}
    ans['num_client'] = num_client
    ans['num_gateway'] = num_gateway
    ans['num_message'] = num_message
    ans['num_sos'] = num_sos
    ans = json.dumps(ans)
    return JsonResponse(ans,safe=False)

def delete_message(request):
    record_id = request.POST.get("record_id")
    obj = Message.objects.get(id = record_id)
    obj.delete()
    return  JsonResponse(None,safe=False)

def delete_user(request):
    record_id = request.POST.get("record_id")
    obj = users.objects.get(id = record_id)
    obj.delete()
    return  JsonResponse(None,safe=False)

def delete_gateway(request):
    record_id = request.POST.get("record_id")
    obj = Gateway.objects.get(id = record_id)
    obj.delete()
    return  JsonResponse(None,safe=False)

def delete_client(request):
    record_id = request.POST.get("record_id")
    obj = Client.objects.get(id = record_id)
    obj.delete()
    return  JsonResponse(None,safe=False)
import base64
import time
def send_it(text):
    headers = {
        "Authorization": "Bearer NNSXS.IDCNMYA7EAI4R5MIZFRQLSDNLABU2BL25HOF44Y.LO5CYOM3WYX45EVVKQQNBKRM5PQ43CVHEXKMKUNT62WWTLCKUVYA",
        "Content-Type": "application/json",
    }

    url = "https://eu1.cloud.thethings.network/api/v3/as/applications/my-new-application-lingmaple/devices/eui-70b3d57ed005c550/down/push"

    data = {
        "downlinks": [{
            "f_port": 42,
        }]
    }
    print(len(text))
    for i in range(len(text)//20+1):
        text1 = base64.b64encode(str(text)[20*i:min(len(text),20*(i+1))].encode("utf-8")).decode("utf-8")
        data["downlinks"][0]["frm_payload"]=text1
        response = requests.post(url, headers=headers, json=data)

        if(response.status_code == 200):
            print("ok")

def send_message(request):
    if request.method == "POST":
        text=request.POST.get("text")
    elif request.method == "GET":
        text = request.GET.get("text")
    send_it(text)
    return HttpResponse()

def update_pwd(request):
    record_id = request.POST.get("record_id")
    obj = users.objects.get(id = record_id)
    obj.pwd_admin = request.POST.get("new_pwd")
    return JsonResponse(None,safe=False)


from django.http import HttpResponse

def my_view(request):
    # 其他逻辑...

    # 获取图片内容（假设是二进制数据）
    image_data = open("/static/images/map.jpg","rb").read()
    
    # 设置响应头，告知浏览器不缓存该图片
    response = HttpResponse(content_type='image/jpeg')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    # 将图片内容写入响应体
    response.write(image_data)
    
    return response


# views.py

import openai
from django.shortcuts import render
from django.http import JsonResponse

def chat_gpt(request):
    if request.method == 'POST':
        user_input = request.POST['input']
        
        # 调用Chat-GPT3.5模型
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        
        reply = response.choices[0].message.content
        
        return JsonResponse({'reply': reply})


import SparkApi

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text = []
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

def chat_api(request):
    #以下密钥信息从控制台获取
    appid = "f2d5e626"     #填写控制台中获取的 APPID 信息
    api_secret = "NzI2ZWZhNWQ1ZDU0M2U0NzJlNzgwYTAw"   #填写控制台中获取的 APISecret 信息
    api_key ="7795760a804419dac26a9133f318c0bf"    #填写控制台中获取的 APIKey 信息

    #用于配置大模型版本，默认“general/generalv2”
    domain = "general"   # v1.5版本
    # domain = "generalv2"    # v2.0版本
    #云端环境的服务地址
    Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
    # Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
    Input = ''
    if (request.method == 'POST'):
        Input = request.POST.get('input')
    elif (request.method == 'GET'):
        Input = request.GET.get('input')
    question = checklen(getText("user",Input))
    SparkApi.answer =""
    #print("星火:",end = "")
    SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    getText("assistant",SparkApi.answer)
    # print(str(text))
    ans ={}
    ans["answer"] = SparkApi.answer
    
    ans["i"] = request.method
    ans = json.dumps(ans)
    return JsonResponse(ans,safe=False)
