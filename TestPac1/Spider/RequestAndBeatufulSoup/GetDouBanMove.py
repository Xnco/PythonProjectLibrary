
# Requests + BeautifulSoup 爬取豆瓣电影Top250

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

}

url = 'https://movie.douban.com/top250'
webdata = requests.get(url, headers=headers)
Soup = BeautifulSoup(webdata.text, 'lxml')

#'#content > div > div.article > ol > li:nth-of-type(1) > div > div.info > div.hd > a > span:nth-of-type(1)'
# li:nth-child(1) > div > div.info > div.bd > div > span:nth-child(4)
allmovies = Soup.select('#content > div > div.article > ol > li')
for movie in allmovies:
    name = movie.find('span', class_='title').get_text()
    star = movie.find('span', class_='rating_num').get_text()
    num = movie.select('div > div.info > div.bd > div > span:nth-of-type(4)')[0].get_text()[:-3]
    text = movie.find('span', class_='inq').get_text()
    info = movie.find('div', class_='bd').select('p')[0].get_text()
    lines = [t.strip() for t in info.strip(' \n').split('\n')]
    line1 =[i.strip(' ') for i in lines[1].split('/')]
    year =line1[0]
    countries =line1[1]
    movietype= [tmp for tmp in line1[2].split()]
    print(movietype)
    # director =
    # action =
