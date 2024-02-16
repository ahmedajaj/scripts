import requests
import time
import math
from bs4 import BeautifulSoup
from multiprocessing import Pool

url = "https://petition.president.gov.ua/petition/152480"
namesList = []

def getInfo (url):

    mainRequest = requests.get(url).content

    title = BeautifulSoup (mainRequest, 'html.parser').find('h1').text
    totalVotes = BeautifulSoup (mainRequest, 'html.parser').find('div', class_='petition_votes_txt').find('span').text
    numberOfPages = math.ceil(int(totalVotes)/30)
    print ("Петиція: " + title + "\n" + "Проголосувало: " + totalVotes + "\n" + "Сторінок: " + str(numberOfPages))
    return numberOfPages

def getNames (x):
    urlVotes = url + "/votes/"
    r = requests.get(urlVotes+str(x))
    soup = BeautifulSoup (r.content, 'html.parser')
    contentPage = soup.find_all('div', class_='table_row')

    internalList = []

    for person in contentPage:
        #number = person.find('div', class_="table_cell number").text
        #date = person.find('div', class_="table_cell date").text

        name = person.find('div', class_="table_cell name").text
        internalList.append(name)
    
    return internalList

    

def saveToFile ():
    flat_list = [x for xs in namesList for x in xs]
    joined_string = "\n".join(sorted(flat_list))

    with open("list_sort3.txt", 'w+') as file:
        file.write(joined_string)
        file.close()


if __name__ == '__main__':
    pages = range(1, getInfo (url)+1)
    threads = 10

    if getInfo (url) > 300: 
        threads = 4

    print(threads)

    with Pool(threads) as pool:
        namesList += pool.map(getNames ,pages)
    saveToFile ()
