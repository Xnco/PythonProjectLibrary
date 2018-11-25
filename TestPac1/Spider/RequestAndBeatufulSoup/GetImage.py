
from bs4 import BeautifulSoup
import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

def GetImage():
    #url = 'https://e-hentai.org/s/0566c066de/1119195-1' #Begin URL
    url = 'https://e-hentai.org/s/88e44c5a4b/1119195-138'

    path = r'H:\e_hentai\Love\55_70\{}.jpg'     #LocalPath
    pageNum = 465
    for num in range(230,pageNum):
        time.sleep(2)
        web_data = requests.get(url, headers=headers)
        Soup = BeautifulSoup(web_data.text, 'lxml')
        alldata = Soup.select('#i3 > a')
        images = alldata[0].select('img')
        url = alldata[0].get('href')        # Next Page
        imageurl = images[0].get('src')     # Image URL
        try:
            content = requests.get(imageurl)# Download
            with open(path.format(num), 'wb') as info:
                info.write(content.content) # Write
                print('Download {} successful, url ： {}'.format(num, imageurl))
        except:
            print('Download {}  failed，url ：{}'.format(num, imageurl))

GetImage()