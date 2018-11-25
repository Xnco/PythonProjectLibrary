#Requests + BeautifulSoup 爬取真实网站

#1 服务器和本地的交换机制
#2 解析真实网页的办法和思路

from bs4 import BeautifulSoup
import requests
import  time

url = 'https://www.tripadvisor.cn/'

#手机页面的header
headers = {
    'Use-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
}

url_outlook = 'https://www.tripadvisor.cn/Attractions-g293920-Activities-c61-Phuket.html'
url_outlook2 =['https://www.tripadvisor.cn/Attractions-g293920-Activities-c61-oa{}-Phuket.html'.format(str(i*30)) for i in range(1,16)]

#主页
def get_index(url):
    web_data = requests.get(url)

    Soup = BeautifulSoup(web_data.text, 'lxml')
    titles = Soup.select('#popularDestinations > div.section > ul.regionContent > li.active > ul > li > div.title > a.cityName')
    images = Soup.select('#popularDestinations > div.section > ul.regionContent > li.active > ul > li > a > span.thumbCrop > img')

    for title, img in zip(titles, images):
        data = {
            'title':title.get_text(),
            'img':img.get('src')
        }
        print(data)

info = []
#吉普岛的户外活动
def get_faws(url):
    web_data = requests.get(url, headers = headers)
    time.sleep(2)
    Soup = BeautifulSoup(web_data.text, 'lxml')

    titles = Soup.select('#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.listing_title > a')
    scores = Soup.select('#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.listing_rating > div > div > span:nth-of-type(1)')
    imgs = Soup.select('img[width="180"]')#获取该尺寸的所有图片
    #imgs = Soup.select('div.thumb.thumbLLR.soThumb > img')#移动端获取图片， 可以获取的到
    reviews = Soup.select('#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.listing_rating > div > div > span.more > a')
    tags = Soup.select('#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.tag_line > div')

    for title, score, img, review, tag in zip(titles, scores, imgs, reviews, tags):

        tmpTags = tag.find_all('span', class_='matchedTag noTagImg')
        list = []
        for tmpTag in tmpTags:
            list.append(tmpTag.get_text())

        data = {
            'title': title.get_text(),
            'score': score.get('alt'),
            'img': img.get('src'),
            'review': review.get_text(),
            'tags':list
        }
        print(data)
        info.append(data)

get_faws(url_outlook)


for tmpURL in url_outlook2:
    get_faws(tmpURL)
    print(len(info))

# Next String Replace
# Get Picture

