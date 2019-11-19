import pandas as pd
import json
import requests

bizon_token = 'Bxt5aOu9rSlgKq6dd9rre-F9TduqrBxGYca_OqrBgQK9pdO5r'

bizon_headers = {'X-Token': bizon_token}

url = "https://online.bizon365.ru/api/v1/webinars/reports/getlist?limit=100"

url2 = "https://online.bizon365.ru/api/v1/webinars/reports/get?webinarId="

answer_from_server =  requests.get(url, headers = bizon_headers) 

json_data = json.loads(answer_from_server.text) 
 


#ищу подходящий id вебинара
elements_in_list = len(json_data['list'])
live_webs = 0
webid = ""
index = 0

while index < elements_in_list and live_webs != 1:
    
    if json_data['list'][index]['type'] == "LiveWebinars":
        live_webs += 1
        webid = json_data['list'][index]['webinarId']
       

    index += 1



def DataFrame_id(id):
    url2 = "https://online.bizon365.ru/api/v1/webinars/reports/getviewers?webinarId="

    get_report = url2 + id + "&skip=0&limit=1000"

    get_report = requests.get(get_report, headers = bizon_headers) 

    json_data1 = json.loads(get_report.text)

    json_data1 = json_data1['viewers']

    df = pd.DataFrame(json_data1)

    print(df)
    
DataFrame_id(webid)


