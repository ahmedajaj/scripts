import requests
import math
from bs4 import BeautifulSoup
import json
import boto3



def send_message(chat_id, text):
    url = "https://api.telegram.org/bot{token}/{method}".format(
        token="535477:xxx",
        method="sendMessage"
    )
    data = {
        "chat_id": chat_id,
        "text": text
    }
    r = requests.post(url, data = data)
    print(r.json())

def lambda_handler(event, context):
    chat_id = event["message"]["from"]["id"]
    url = event["message"]["text"]
    urlVotes = url + "/votes/"
    mainRequest = requests.get(url).content
    
    title = BeautifulSoup (mainRequest, 'html.parser').find('h1').text
    totalVotes = BeautifulSoup (mainRequest, 'html.parser').find('div', class_='petition_votes_txt').find('span').text
    numberOfPages = math.ceil(int(totalVotes)/30)
    response = "Петиція: " + title + "\n" + "Проголосувало: " + totalVotes + "\n" + "Сторінок: " + str(numberOfPages)
    
    send_message(chat_id, response)
    
    
    list = []

    for x in range(1,numberOfPages+1):
        r = requests.get(urlVotes+str(x))
        soup = BeautifulSoup (r.content, 'html.parser')
    
        contentPage = soup.find_all('div', class_='table_row')
        
        print (x)
    
        for person in contentPage:
            #number = person.find('div', class_="table_cell number").text
            name = person.find('div', class_="table_cell name").text
            #date = person.find('div', class_="table_cell date").text
    
            list.append(name + " / " +str(x) )
    
    
    joined_string = "\n".join(sorted(list))

    file_name = "list.txt"
    lambda_path = "/tmp/" + file_name
    
    with open(lambda_path, 'w+') as file:
        file.write(joined_string)
        file.close()
    
    s3 = boto3.client('s3')
    s3.upload_file(lambda_path, 'petitiontelegrambot', file_name)
    
    
    urlSend = "https://api.telegram.org/bot{token}/{method}".format(
        token="5354769467:AAG7d1IOnR7BqOwsZ78mYi06s1LX6_IrUfk",
        method="sendDocument"
    )
    
    dataSend = {"chat_id": chat_id}
    files = {'document': open(lambda_path, 'rb')}
    
    r2 = requests.post(urlSend, data = dataSend, files=files)
    print(r2.json())

    return {
        "statusCode": 200,
        "body": "{'Test': 'Test'}",
        "headers": {
            'Content-Type': 'text/html',
        }
    }
