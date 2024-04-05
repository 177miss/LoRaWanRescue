import sys
from appexpress.models import Message
import requests
import json
import base64
import random
import AIchat
from appexpress.views import send_it


def get_json(file_content):
    result={}
   
    try:
        data_dict = json.loads(file_content)
        result['name']=data_dict['result']['name']
        if result['name']=="ns.down.join.schedule.success" or result['name']=="as.up.data.forward":
            if(result['name']=="ns.down.join.schedule.success"):
                return result
            else:
                try:
                    result['time']=data_dict['result']['time']
                    result['arrive_time']=data_dict['result']["data"]['received_at']
                    result['device_id']=data_dict['result']["identifiers"][0]["device_ids"]["dev_eui"]
                    result['gateway_id']=data_dict['result']['data']["uplink_message"]["rx_metadata"][0]["gateway_ids"]["eui"]
                    result['message_id']=data_dict['result']["unique_id"]
                    result['message']=base64.b64decode(data_dict['result']['data']["uplink_message"]["frm_payload"]).decode('utf-8').strip()
                    
                except:
                    return None
        else:
            result=None
    except:
        return None    
    return result

url = 'https://eu1.cloud.thethings.network/api/v3/events'

headers = {
    'Authorization': 'Bearer NNSXS.IDCNMYA7EAI4R5MIZFRQLSDNLABU2BL25HOF44Y.LO5CYOM3WYX45EVVKQQNBKRM5PQ43CVHEXKMKUNT62WWTLCKUVYA',
    'Accept': 'text/event-stream',
    'Content-Type': 'application/json'
}

data = {
    "identifiers": [{
        "application_ids": {"application_id": "my-new-application-lingmaple"}
    }],
    "tail": 0,

}

def model_add(s):
    if(s['name']=="ns.down.join.schedule.success"):
        new_object=Message(Time=s['time'],Name=s["name"])
    else:
        new_object=Message(Time=s['time'],Eui=s["message_id"],Name=s["name"],Client=s['device_id'],Gateway=s["gateway_id"],Arrtime=s['arrive_time'],Text=s["message"],latitude=random.uniform(24.8,40.0),longitude = random.uniform(100.0,115.0))
        if(s["message"][0] == '?' or s["message"][0] == "？"):
            index = s["message"].find("@")
            ques = s["message"][1:index]
            ans = AIchat.AIanswer(ques)
            print(ans)
            send_it(ans)
    new_object.save()      

    
    
    
response = requests.post(url, headers=headers, json=data, stream=True)
print("我要开始喽")
for line in response.iter_lines():
    s=get_json(line)
    print(s)
    if s!=None:
        model_add(s)      