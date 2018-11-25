# -*- coding: UTF-8 -*-

import requests
import time
from bs4 import BeautifulSoup
from openpyxl import Workbook
from win32com.shell import shell, shellcon

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"

}

def GetDesktopPath():
    ilist =shell.SHGetSpecialFolderLocation(0, shellcon.CSIDL_DESKTOP)
    return shell.SHGetPathFromIDList(ilist)

def GetUrlAddress(url, ws, loadNum):
    data = requests.get(url, headers=headers)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text, 'lxml')
    # 读取该页面所有的职业信息
    allcompany = soup.select('.newlist')

    num = 0
    for company in allcompany:
        data = []
        # 职位名称
        zwmc = company.find('td', 'zwmc')
        if zwmc is not None:
            workname = zwmc.find('a').get_text()
            data.append(workname)
        # 公司名字, 公司招聘页面
        gsmc = company.find('td', class_="gsmc")
        if gsmc is not None:
            tmpa = gsmc.find('a')
            if tmpa is not None:
                name = tmpa.get_text()
                web = tmpa.get('href')
                data.append(name)
                data.append(web)
        # 薪资
        zwyx = company.find('td', class_="zwyx")
        if zwyx is not None:
            money = zwyx.get_text()
            data.insert(2,money)
        # 工作地点
        gzdd = company.find('td', class_='gzdd')
        if gzdd is not None:
            address = gzdd.get_text()
            data.insert(3, address)
        # 公司性质, 公司规模, 学历要求, 工作经验
        other = company.find('li', class_ = 'newlist_deatil_two')
        if other is not None:
            all = other.select('span')

            data.insert(3, "没写")  # 工作经验
            data.insert(4, "没写")  # 学历
            data.insert(6, "没写")  # 公司性质
            data.insert(7, "没写")  # 公司规模

            for item in all:
                text = item.get_text().split("：")
                if text[0] == "公司性质":
                    data[6] = text[1]
                if text[0] == "公司规模":
                    data[7] = text[1][:-1]
                if text[0] == "学历":
                    data[4] = text[1]
                if text[0] == "经验":
                    data[3] = text[1]

        if len(data) == 9:
            ws.append(data)
            num = num + 1

    # 判断是否加载成功当前页面 - 加载失败重新加载, 最多加载3次,3次还失败就不加载了

    if loadNum <= 3:
        if num == 0:
            print("加载第{}次失败, 休息一会, 地址是{}".format(loadNum, url))
            time.sleep(2)
            loadNum = loadNum + 1
            GetUrlAddress(url, ws, loadNum)
            return

    # 判断是否有下一页
    nextpage = soup.find('a', class_='next-page')
    tmphref = nextpage.get('href')
    if tmphref is not None:
        #nextUrl = nextpage.get('href') # 下一页被加密, 用规律查找
        nextUrl = url[:-1] + str(int(url[-1:])+1) # 页码+1
        print("加载成功, 休息一下, 准备下一页吧, 地址是{}".format(nextUrl))
        time.sleep(2)  # 如果有下一页休息2秒在爬下一页
        GetUrlAddress(nextUrl,ws,1)
    else:
        print("没有下一页了, 加载结束")

if __name__ == '__main__':
    wb = Workbook()
    ws = wb.active
    ws.append(["职位名称","公司名", "月薪", "工作经验","学历", "工作地点", "公司性质", "公司规模", "公司招聘页面"])

    # http://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&kw=unity&p=1
    address = "南京"
    keyword = "unity"
    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl={}&kw={}&p=1'.format(address, keyword)
    GetUrlAddress(url, ws, 1)

    path = GetDesktopPath() # 桌面地址
    wb.save(path.decode() + "/test.xlsx")

