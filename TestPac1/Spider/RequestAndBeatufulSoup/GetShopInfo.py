# 获取图片地址 价格 商品标题 评分量 评分星级

from bs4 import BeautifulSoup

info = []

path = r'F:\PythonProject\Plan-for-combating-master\week1\1_2\1_2answer_of_homework\1_2_homework_required\index.html'
with open(path, 'r', encoding='utf-8') as web_data:
    Soup = BeautifulSoup(web_data, 'lxml')  #网站解析

    images = Soup.select('body > div > div > div.col-md-9 > div > div > div > img')                         #图片
    prices = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right') #价格
    titles = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a')        #标题
    reviews = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right') #评分量
    star = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p > span')        #5*n个星
    sTest = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p:nth-of-type(2)')

    #先获取父级的tag, 再获取所有符合条件子集的长度
    sNum = []
    for i in sTest:
        sNum.append(len(i.find_all('span', class_='glyphicon glyphicon-star')))

    print('------------------星星第一种方法结束-----------------')

    for i in range(0,8):
        data = {
            'img':images[i],
            'price':prices[i].get_text(),
            'title':titles[i].get_text(),
            'review':reviews[i].get_text(),
            'star':star[i*5:(i+1)*5],
            'starNum':sNum[i]
        }
        info.append(data)

    #将不是空的数出来， 共32个
    num = 0
    for i in star:
        print(i.attrs)
        if i.attrs['class'][1] == 'glyphicon-star':
            num = num + 1
    print(num)

print('-------------最后总结--------------')

num = 0
for i in info:
    num = num + i['starNum']

print(num)

'''
    n = 1
    for num in i['star']:
        print('{}-{}'.format(n, num))
        n = n + 1
'''