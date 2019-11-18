from urllib import  parse
import requests
import json
import datetime
import time


bizon_token = 'Bxt5aOu9rSlgKq6dd9rre-F9TduqrBxGYca_OqrBgQK9pdO5r'

bizon_headers = {'X-Token': bizon_token}

url = "https://online.bizon365.ru/api/v1/webinars/reports/getlist?limit=100"

answer_from_server =  requests.get(url, headers = bizon_headers) 

json_data = json.loads(answer_from_server.text) 
 

 
#пока создал предположительный JSON файл, который должен прийти с сервера
#тк получить с сервера нет возможности
#далее следующие две строчки нужно удалить 
#json_data = '{"skip": 0, "limit": 100, "count": 100, "list": [{"name": "123", "webinarId": "webid", "type": "LiveWebinars", "created": "2013-02-25T18:25:10", "count1": 1234, "count2": 321}]}'
#json_data = json.loads(json_data)





elements_in_list = len(json_data['list'])
viewers = 0 
live_webs = 0
auto_webs = 0
duration_of_webinar = 0
index = 0

while index < elements_in_list:
    duration_of_webinar += json_data['list'][index]['count2']
    if json_data['list'][index]['type'] == "LiveWebinars":
        live_webs += 1
        viewers += json_data['list'][index]['count1']
       
    else:
        auto_webs += 1
        
    index += 1

avg_viewers = round(viewers / live_webs)

avg_duration_of_webinar = duration_of_webinar / (live_webs + auto_webs)

seconds = round(avg_duration_of_webinar, 3) * 60  



print("Количество живых вебинаров: " + str(live_webs))

print("Количество авто вебинаров: " + str(auto_webs))

print("Среднее количество участников на вебинарах: " + str(avg_viewers))

print("Средняя длина вебинара: " + str(datetime.timedelta(0, seconds)))