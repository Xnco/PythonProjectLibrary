from bs4 import BeautifulSoup
import requests

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'UM_distinctid=162f5f44f0113-0313b684ffd29e-5e4c2719-100200-162f5f44f05116; __jsluid=d26199ff490223142ead3dca3b417f0d; PHPSESSID=rcqhhvqkvd9ggs9mqarotu54n7; CNZZDATA1272873895=1502087634-1524539933-null%7C1524545333',
'Host': 'm.biquge.com.tw',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}

def LoadSinglePage(url):
    data = requests.get(url)
    data.encoding = "utf-8"
    soup = BeautifulSoup(data.text, 'lxml')

    content = soup.select('.box_con')[0]
    text = content.select('#content')[0]
    print(text.text.encode('UTF-8'))

LoadSinglePage("http://www.biquge.com.tw/16_16611/8617667.html")