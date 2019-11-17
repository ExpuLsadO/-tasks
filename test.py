from urllib import  parse
import requests
import json
import datetime
import time
url = "https://online.bizon365.ru/api/v1/webinars/reports/getlist?limit=100"

answer_from_server =  requests.get(url) 

json_data = json.loads(answer_from_server.text) 
 

 
 #пока создал предположительный JSON файл, который должен прийти с сервера
 #тк получить с сервера нет возможности
 #далее следующие две строчки нужно удалить 
json_data =  '{"skip": 0, "limit": 100, "count": 100, "list": [{"name": "123", "webinarId": "webid", "type": "LiveWebinars", "created": "2013-02-25T18:25:10", "count1": 1234, "count2": 321}]}'
json_data = json.loads(json_data)



number_of_elements_in_list =0
for results in json_data['list']:
    number_of_elements_in_list+=1


number_of_viewers = 0 
number_of_live_webs = 0
number_of_auto_webs = 0
duration_of_webinar = 0
index_of_element_in_list = 0

while index_of_element_in_list < number_of_elements_in_list:
    duration_of_webinar += json_data['list'][index_of_element_in_list]['count2']
    if json_data['list'][index_of_element_in_list]['type'] == "LiveWebinars":
        number_of_live_webs+=1
        number_of_viewers += json_data['list'][index_of_element_in_list]['count1']
       
    else:
        number_of_auto_webs+=1
        
    index_of_element_in_list+=1

average_number_of_viewers = number_of_viewers / number_of_live_webs

average_duration_of_webinar = duration_of_webinar / (number_of_live_webs + number_of_auto_webs)

seconds = average_duration_of_webinar * 60  


print("Количество живых вебинаров: " + str(number_of_live_webs))

print("Количество авто вебинаров: " + str(number_of_auto_webs))

print("Среднее количество участников на вебинарах: " + str(average_number_of_viewers))

print("Средняя длина вебинара: " + str(datetime.timedelta(0, seconds)))