import requests
import time, threading
from bs4 import BeautifulSoup

baseURL = "http://www.gggg00.pw/gggg2/14.html"

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
}

web_data = requests.get(baseURL, headers = headers)

Soup = BeautifulSoup(web_data.text, 'lxml')

root = Soup.select("body > div:nth-of-type(9) > div > ul > li:nth-of-type(15) > a")

for text in root:
    print(text.get('href'))

#Fuck
