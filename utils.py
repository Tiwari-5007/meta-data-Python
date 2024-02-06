import requests
import json
from logsHandler import logw

def sendmetaData(decoded_data):
  try:
    if decoded_data.endswith('"'):
        raw_data = decoded_data.rstrip('"')
    else:
        raw_data = decoded_data
    meta_data = eval(raw_data.split('@@')[1])
    url = meta_data['url']
    #payload = json.loads(meta_data['payload'])
    payload = meta_data['payload']
    headers = meta_data['headers']
    payload = json.dumps(payload)
    logw("info",f"Payload:   {payload}\n")
    response = requests.request("POST", url, headers=headers, data=payload)
    get_content = f"Response:    {response.json()}\n"
    logw("info",f" Data has been sent    STATUS CODE: {response.status_code}    {payload}\n{get_content}\n")
    #print("info",f"Data has been sent    STATUS CODE: {response.status_code}    {payload}\n{get_content}\n")
  except Exception as e:
    #print(f"Error:               123    :   {e}\n")
    logw("error",f"Error: {e}\n")
