import pandas as pd
import json
import requests
from google.cloud import bigquery
from google.oauth2 import service_account

pd.options.display.max_rows = 5000
pd.options.display.max_columns = 5000

bizon_token = 'Bxt5aOu9rSlgKq6dd9rre-F9TduqrBxGYca_OqrBgQK9pdO5r'

bizon_headers = {'X-Token': bizon_token}

url = "https://online.bizon365.ru/api/v1/webinars/reports/getlist?limit=100" # getlist

url2 = "https://online.bizon365.ru/api/v1/webinars/reports/getviewers?webinarId=" # getviewers

url3 = "https://online.bizon365.ru/api/v1/webinars/reports/get?webinarId=" # get

answer_from_server =  requests.get(url, headers = bizon_headers) 

json_data = json.loads(answer_from_server.text) 


def webinars ():
    json_data = json.loads(answer_from_server.text) 

    json_data = json_data['list']

    df = pd.DataFrame(json_data, columns = ['webinarId', 'type', 'count1', 'count2'])

    df.columns = ['webinarId', 'type', 'viewers_number', 'duration']

    return df

df = webinars()

def reports (id):

    get_report = url2 + id + "&skip=0&limit=1000"

    get_report = requests.get(get_report, headers = bizon_headers) 

    json_data = json.loads(get_report.text)

    json_data = json_data['viewers']

    df = pd.DataFrame(json_data, columns = ['chatUserId', 'webinarId', 'username', 'phone', 'country', 'city', 'ip', 'view', 'viewTill', 'mob', 'clickFile', 'utm_source' ])

    df.columns = ['Id', 'Webinar_Id', 'Name', 'Phone', 'Country', 'City', 'IP', 'Start_time', 'Finish_time', 'Mob', 'Click', 'Utm' ]
    
    return df

 

def messages (id):
    get_report = url3 + id 

    get_report = requests.get(get_report, headers = bizon_headers) 

    json_data = json.loads(get_report.text)

    json_data = json_data['report']
    
    json_data1 = json_data['messages'] 

    json_data2 = json_data['messagesTS']

    json_data1 = json.loads(json_data1)
    
    json_data2 = json.loads(json_data2)
    
    df = pd.DataFrame( columns = ['id', 'message', 'ts']) 
    
    
    j = 0 # индекс элемента в датафрейме
    for i in json_data1:
        
        k = 0 # счетчик комментариев одного пользователя
        while k != len(json_data1[i]): # заполняем пустой датафрейм
            df.loc[j] ={ 'id': i, 'message': json_data1[i][k], 'ts': ''}
            k +=1
            j +=1
    
    j = 0 # индекс элемента в датафрейме
    for i in json_data2:
        
        k = 0 # счетчик комментариев одного пользователя
        while k != len(json_data2[i]): # заполняем столбец времени в датафрейме
            df.loc[j,'ts'] = json_data2[i][k] 
            k +=1
            j +=1
        
    return df

Df = pd.DataFrame() # все репорты будут тут 
Df_m = pd.DataFrame() # все сообщения будут тут
#ищу подходящий id вебинара
elements_in_list = len(json_data['list'])
webid = ""
index = 0
c_live = 0
while index < elements_in_list and c_live !=2: # отчет есть только о первых двух вебинарах(на 25.11.2019 нет ни одного доступного отчета)
    if json_data['list'][index]['type'] == "LiveWebinars":
        webid = json_data['list'][index]['webinarId']
        
        d = reports(webid)
        
        d_m = messages(webid)

        if c_live == 0:
            Df = d
            Df_m = d_m 
        else:
            Df = pd.concat([Df, d], ignore_index = True)
            Df_m = pd.concat([Df_m, d_m], ignore_index = True)
        
        c_live += 1

    index += 1

# таблица с информацией о всех вебах(уже создана)
df.to_gbq('dataset.webinars', project_id = 'expulsado-project', if_exists = 'append', private_key = 'C:\\Users\\Александр\\Downloads\\My Project -6896200f98d3.json')

# таблица с информацией о всех комментариях (не добавлена в bigquery, так как нет доступа отчетам по вебам)
Df_m.to_gbq('dataset.messages', project_id = 'expulsado-project', if_exists = 'append', private_key = 'C:\\Users\\Александр\\Downloads\\My Project -6896200f98d3.json')

# таблица с информацией о пользователях со всех вебов (не добавлена в bigquery, так как нет доступа отчетам по вебам)
Df.to_gbq('dataset.reports', project_id = 'expulsado-project', if_exists = 'append', private_key = 'C:\\Users\\Александр\\Downloads\\My Project -6896200f98d3.json')

# проверка на то, что отдает каждая из функций 
# print(df)
# print("\n\n\n")
# print(Df)
# print("\n\n\n")
# print(Df_m)