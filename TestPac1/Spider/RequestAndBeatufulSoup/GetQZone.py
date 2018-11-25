
import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

}

url = 'https://user.qzone.qq.com/331450488/infocenter'

webdata = requests.get(url, headers=headers)
Soup = BeautifulSoup(webdata.text, 'lxml')
#                   '#msgList > li:nth-child(1) > div.box.bgr3 > div.bd > pre'
#test = Soup.select('#msgList > li:nth-of-type(1) > div.box.bgr3 > div.bd > pre')

#data = Soup.find_all('div', class_='bd')
#print(data)

print(webdata.text)