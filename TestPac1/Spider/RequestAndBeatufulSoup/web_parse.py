
from bs4 import BeautifulSoup

info = []

with open(r'H:\Python\Plan-for-combating-master\week1\1_1\1_1code_of_video\mHomework.html', 'r', encoding='utf-8') as web_data:
    Soup = BeautifulSoup(web_data, 'lxml')

    titles = Soup.select('head > title')
    image = Soup.select('body > div.main-content > ul > li > img')      #具体的img
    textTitle = Soup.select('body > div.main-content > ul > li > h3')   #具体的h3
    text = Soup.select('body > div.main-content > ul > li ') #获取父标签下的所有子标签的信息

    #print(titles ,image, textTitle,text,  sep="\n--------------------------\n")

for i, tT, t in zip( image, textTitle, text):
    data = {
        'textTitle':tT.get_text(),  #获取文本信息
        'text':list(t.stripped_strings), #将获取的多个信息列表化，获取所有string
        'image':i.get('src')        #获取图片信息
    }
    print(data)
    info.append(data)  #将信息存储到列表中

#遍历列表， 并筛选信息
for t in info:
    for text in t['text']:
        if text == '周杰伦':
            print('终于等到你')