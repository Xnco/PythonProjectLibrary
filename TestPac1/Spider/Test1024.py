import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",

    'Referer':'http://cc.itbb.men/thread0806.php?fid=16'
}

data = requests.get('http://cc.itbb.men/htm_data/16/1804/3101094.html', headers=headers)

print(data.content)