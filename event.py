import requests
import json

application_api = 'NNSXS.IDCNMYA7EAI4R5MIZFRQLSDNLABU2BL25HOF44Y.LO5CYOM3WYX45EVVKQQNBKRM5PQ43CVHEXKMKUNT62WWTLCKUVYA'
user_api = 'NNSXS.7FOUWVAUBFQG66NDUXECOEZ3Y2HRFMDQCU6GL6I.3KADRNSNLFT35YU7DSB4DWSY5M5DLCPOLJCRGGO7BMK5DYVTHZ2Q'

application_headers = {
    'Authorization': 'Bearer {}'.format(application_api),
    'Content-Type':'text/event-stream',
    'Accept': 'text/event-stream'
}

user_headers = {
    'Authorization': 'Bearer {}'.format(user_api),
}

EndDeviceRegistryList_url = 'https://eu1.cloud.thethings.network/api/v3/applications/{}/devices'.format('my-new-application-lingmaple')

EventsStream_url = 'https://eu1.cloud.thethings.network/api/v3/events'

response = requests.post(url=EventsStream_url,headers=user_headers,stream=True)

if response.status_code == 200:
    print(response.status_code)
    print(response.content)
    print(response.text)
    print(response.raw)
    
    
else:
    print('Status code: {}'.format(response.status_code))