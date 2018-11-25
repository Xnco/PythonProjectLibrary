# -*- coding: utf-8 -*-
import os, time, random
import requests
from multiprocessing import Process, Pool
from bs4 import BeautifulSoup
from openpyxl import Workbook

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",

    'Referer':'http://cc.itbb.men/thread0806.php?fid=16'
}

#http://cc.itbb.men/thread0806.php?fid=16&search=&page=2

dyUrl = 'http://cc.itbb.men/'
base_url = dyUrl + 'thread0806.php?fid=16&search=&page='
# 存在本地的路径
localpath = 'H:/e_hentai/cl/ddedqz'
# 错误列表
failedpath = 'H:/e_hentai/cl/failed.xlsx'
allUrl = []

def GetAllUrl(url, num):
    try:
        newurl = url + str(num)
        html_data = requests.get(newurl, headers=headers)
        html_data.encoding = 'utf-8'
        Soup = BeautifulSoup(html_data.content, 'lxml')
        ajaxtable = Soup.select('#ajaxtable')[0]
        urlList = ajaxtable.select('tbody > tr > td > a[target="_blank"]')

        # 信息获取到后创建文件夹 H:/e_hentai/cl/ddedqz
        has = os.path.exists(localpath)
        if not has:
            os.makedirs(localpath)

        for iurl in urlList:
            # 当页所有地址
            tmpUrl = dyUrl + iurl['href']

            allUrl.append(tmpUrl) # 不直接获取, 先存到集合中
            # GetTargetAllImage(tmpUrl)

        '''获取下一页的备用方案'''
        # pages = Soup.select('.pages > a')
        # for page in pages:
        #     # 获取下一页, 不支持 UTF-8
        #     # ÏÂÒ»í" = 下一頁
        #     if page.get_text() == "下一頁":
        #         nexturl = page['href']

    except:
        print("获取 {} 的数据失败.Next--->".format(url + str(num)))

    time.sleep(round(random.uniform(0.5,1.5), 2))

#获取目标网页所有的图片
def GetTargetAllImage(url):
    try:
        with requests.get(url, headers=headers) as html_data:
            html_data.encoding = 'utf-8'

            Soup = BeautifulSoup(html_data.content, 'lxml')
            title = Soup.select('#main > div.t')[0].text[13:]  # 标题
            newpath = '{}/{}'.format(localpath, title).strip(' \n\r')
            has = os.path.exists(newpath)
            if not has:
                os.makedirs(newpath)
                allimage = Soup.find_all('input', type='image')
                num = 1
                wb = Workbook()
                ws = wb.active
                ws.append([url])
                for image in allimage:
                    try:
                        imageurl = image['src']
                        imagepath = '{}/{}.jpg'.format(newpath, str(num))
                        DownLoadImage(imageurl, imagepath)
                        time.sleep(round(random.uniform(0.2,6), 2))
                        num += 1
                        ws.append([imageurl])

                    except:
                        print("图片地址获取失败")
                wb.save(newpath + '/url.xlsx')
            else:
                print("该套图 {} 已存在".format(url))
    except:
        print("获取 {} 图片失败".format(url))

def DownLoadImage(url, path):
    try:
        # Download Image
        with requests.get(url, headers=headers) as data:
            with open(path, 'wb') as info:
                info.write(data.content)
                print('Download {} successful'.format(path))
    except:
        print('Download {} failed, url = {}'.format(path, url))

# 暂时用固定顺序获取下一页

if __name__=='__main__':
    for pageNum in range(1,100):
        GetAllUrl(base_url, pageNum)
    print(len(allUrl))
    p = Pool(4)
    for url in allUrl:
        p.apply_async(GetTargetAllImage, args=(url,))
    p.close()
    p.join()


