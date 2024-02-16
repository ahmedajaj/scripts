import requests
import math
from bs4 import BeautifulSoup
from multiprocessing import Pool
import boto3

API_URL = "https://api.telegram.org/bot5354769467:AAG7d1IOnR7BqOwsZ78mYi06s1LX6_IrUfk"
S3_BUCKET = "petitiontelegrambot"
FILE_NAME = "list.txt"
FILE_PATH = "/tmp/" + FILE_NAME

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }
    r = requests.post(url, data = data)
    print(r)

def send_document(chat_id, document_path):
    url = f"{API_URL}/sendDocument"

    data = {"chat_id": chat_id}
    files = {'document': open(document_path, 'rb')}
    
    r = requests.post(url, data = data, files = files)
    print(r)


def createFile (namesList): 
    flat_list = [x for xs in namesList for x in xs]
    joined_string = "\n".join(sorted(flat_list))

    with open(FILE_PATH, 'w+') as file:
        file.write(joined_string)
        file.close()

    s3 = boto3.client('s3')
    s3.upload_file(FILE_PATH, S3_BUCKET, FILE_NAME)

def getInfo (url):
    mainRequest = requests.get(url).content

    title = BeautifulSoup (mainRequest, 'html.parser').find('h1').text
    totalVotes = BeautifulSoup (mainRequest, 'html.parser').find('div', class_='petition_votes_txt').find('span').text
    numberOfPages = math.ceil(int(totalVotes)/30)
    
    return title, totalVotes, numberOfPages

def getNames (x):
    r = requests.get(URL + "/votes/" + str(x))
    soup = BeautifulSoup (r.content, 'html.parser')
    contentPage = soup.find_all('div', class_='table_row')

    internalList = []

    for person in contentPage:
        #number = person.find('div', class_="table_cell number").text
        #date = person.find('div', class_="table_cell date").text

        name = person.find('div', class_="table_cell name").text
        internalList.append(name)
    
    return internalList

def lambda_handler(event, context):
    if __name__ == '__main__':
        CHAT_ID = event["message"]["from"]["id"]
        URL = event["message"]["text"]
        
        title, totalVotes, numberOfPages = getInfo (URL)
        response = "Петиція: " + title + "\n" + "Проголосувало: " + totalVotes + "\n" + "Сторінок: " + str(numberOfPages)
        send_message(CHAT_ID, response)

        pages = range(1, numberOfPages+1)
        
        threads = 10
        if numberOfPages > 300: 
            threads = 4

        print(threads)

        namesList = []
        with Pool(threads) as pool:
            namesList += pool.map(getNames ,pages)

        createFile (namesList)
        send_document(CHAT_ID, FILE_PATH)
    
        return {
            "statusCode": 200,
            "body": "{'Test': 'Test'}",
            "headers": {
                'Content-Type': 'text/html',
            }
        }