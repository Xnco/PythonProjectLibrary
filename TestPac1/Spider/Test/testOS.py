from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from bs4 import BeautifulSoup
import requests
import time

# 爬取豆瓣读书的Top250信息 - 并保存到Excel中

beginUrl = "https://book.douban.com/top250?start=0"

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
    "Host":"book.douban.com",
    "Referer":"https://book.douban.com/",
}

allURL = []

CountryInfo = {
    '英':'英国',
    '法':'法国',
    '日':'日本',
    '俄':'俄国',
    '美':'美国',
    '澳':'澳大利亚',
    '英':'英国',
    '捷克':'捷克',
    '清':'中国',
}

# 遍历榜单所有的页码，直到没有下一页为止，保存每本书的url
def GetAllBookURl(url):
    tmp_data = requests.get(url, headers=headers)
    tempSoup = BeautifulSoup(tmp_data.content, 'lxml')
    curAllUrl = tempSoup.select(".nbg")

    for tmpurl in curAllUrl:
        allURL.append(tmpurl['href'])

    curNext = tempSoup.select('.next')[0].select('a')
    if len(curNext) == 0:
        return
    else:
        nextUrl = curNext[0]['href']
        time.sleep(0.3)
        GetAllBookURl(nextUrl)

def GetSingleBook(url, num):
    try:
        tmp_data = requests.get(url, headers=headers)
        tmpSoup = BeautifulSoup(tmp_data.content, 'lxml')

        tmpbook = []
        tmpbook.append(num)
        tmpbody = tmpSoup.select('#wrapper')[0]
        tmpbook.append(tmpbody.select('h1 > span')[0].get_text())  # 获取书名
        authorinfo = tmpbody.select('#info > a')[0].get_text()  # 作者信息
        infos = authorinfo.split(']')
        if len(infos) == 1:
            # 中国人，没有[]
            tmpbook.append(infos[0].strip(' []【】著\n'))
            tmpbook.append("中国")
        elif len(infos) == 2:
            # 外国人有[]
            tmpbook.append(infos[1].strip(' []【】著\n'))
            country = infos[0].strip(' []【】著\n')
            try:
                tmpbook.append(CountryInfo[country])
            except:
                tmpbook.append('未知')
        else:
            tmpbook.append('未知')
            tmpbook.append("未知")

        tmpstar = tmpSoup.select('#interest_sectl')[0];

        score = tmpstar.select('div > div.rating_self.clearfix > strong')[0].get_text()
        tmpbook.append(score)  # 分数

        people =tmpstar.select('div > div.rating_self.clearfix > div > div.rating_sum > span > a > span')[0].get_text()
        tmpbook.append(people)  # 评分人数

        return tmpbook
    except:
        return []


GetAllBookURl(beginUrl)

print('获取所有的书本网页， 共{}本书'.format(len(allURL)))

wb = Workbook()
ws = wb.active
ws.append(['编号','书名','作者','国籍','评分','评分人数'])

num = 1
for url in allURL:
    book = GetSingleBook(url, num)
    if len(book) != 0:
        ws.append(book)
        print("保存 {} 信息成功".format(book[1]))
        time.sleep(0.5)
        num = num + 1
    else:
        print('书籍信息错误')
# 保存到 excel 中, path -> H:/TestFile/Top250Book.xlsx
wb.save('H:/TestFile/Top250Book.xlsx')


