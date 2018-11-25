
import requests
from lxml import html
import os
import time

path = 'H:\e_hentai\meiziwang'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Referer' : 'http://www.mzitu.com',
}

#获取主页列表
def GetPage(baseurl):
    web_data = requests.get(baseurl)
    selector = html.fromstring(web_data.content)

    urls = []
    for i in selector.xpath('//ul[@id="pins"]/li/a/@href'):
        urls.append(i)
    return urls

#获取当前页的页码信息
def GetPageInfo(url):
    info = html.fromstring(requests.get(url).content)
    title = info.xpath('//h2[@class="main-title"]/text()')[0]
    pageSum = info.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]

    jpgURLs = []
    for i in range(int(pageSum)):
        tmpURL = '{}/{}'.format(url, i+1)
        imgDate = html.fromstring(requests.get(tmpURL, headers=headers, timeout=500).content)
        jpgurl = imgDate.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        jpgURLs.append(jpgurl)
    return title, jpgURLs

#获取图片并下载
def GetImageAndDownLoad(title, jpgURLs):
    num = 1
    count = len(jpgURLs)

    dirName = '{}\【{}P】 {}'.format(path, str(count), title)
    #dirName = u"【%sP】%s" % (str(count), title)

    try:
        os.mkdir(dirName)   #创建文件夹
    except:
        print("文件存在，跳过")
        return

    for i in jpgURLs:
        filename = '{}/{}.jpg'.format(dirName,num)
        print('开始下载图片：{}的第{}/{}张, 图片地址为: {}'.format(title, num, count, i))

        with open(filename, 'wb') as jpg:
            jpg.write(requests.get(i, headers=headers, timeout=500).content)
            time.sleep(2)
        num += 1
    print('下载完毕， 生成地址文件')

    txtName = '{}/url.txt'.format(dirName)
    with open(txtName, 'w') as text:
        text.write('\n'.join(jpgURLs))

base = "http://www.mzitu.com/page/{}/"

allinfo = []
for i in range(1,161):
    tmpurl = base.format(i)
    urls = GetPage(tmpurl)

    for url in urls:
        info = GetPageInfo(url)
        allinfo.append(info)

print('Begin Download')
print(len(allinfo))
for tmpinfo in allinfo:
    GetImageAndDownLoad(tmpinfo[0], tmpinfo[1])



