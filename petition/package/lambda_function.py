import requests
import math
from bs4 import BeautifulSoup


url = "https://petition.president.gov.ua/petition/141740"
urlVotes = url + "/votes/"

mainRequest = requests.get(url).content

title = BeautifulSoup (mainRequest, 'html.parser').find('h1').text
totalVotes = BeautifulSoup (mainRequest, 'html.parser').find('div', class_='petition_votes_txt').find('span').text
numberOfPages = math.ceil(int(totalVotes)/30)
print ("Петиція: " + title + "\n" + "Проголосувало: " + totalVotes + "\n" + "Сторінок: " + str(numberOfPages))