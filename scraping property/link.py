# coding=utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import random
import datetime
import pandas as pd

context = ssl._create_unverified_context()
random.seed(datetime.datetime.now())
regionPages = []
areaPages = []
def getRegionLinks():
    html = urlopen("https://transactions.gohome.com.hk/en/",context=context)
    bsObj = BeautifulSoup(html,"lxml")
    for link in bsObj.find("div",{"class":"navWrap"}).findAll("a",href=re.compile("//transactions.gohome.com.hk/")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in regionPages:
                newPage = link.attrs['href']
                print(newPage.split("/")[3])
                regionPages.append(newPage.split("/")[3])



def getAreaLinks(URL):
    html = urlopen("https://transactions.gohome.com.hk/"+URL+"/en",context=context)
    bsObj = BeautifulSoup(html,"lxml")
    for link in bsObj.find("table", {"width": "640"}).findAll("a", href=re.compile("//transactions.gohome.com.hk/records/")):
        if 'href' in link.attrs:
            if link.attrs['href'].replace(' ','') not in areaPages:
                newPage = link.attrs['href'].replace(' ','')
                print(newPage)
                areaPages.append(newPage)
                html1 = urlopen("https:"+newPage,context=context)
                bsObj1 = BeautifulSoup(html1,"lxml")
                for link1 in bsObj1.findAll("a", href=re.compile("/?Page=")):
                    newPage1 = "//transactions.gohome.com.hk"+link1.attrs['href']
                    if newPage1.replace(' ','') not in areaPages:
                        print(newPage1.replace(' ',''))
                        areaPages.append(newPage1.replace(' ',''))

def getLinks():
    getRegionLinks()
    for link in regionPages:
        getAreaLinks(link)
    save = pd.DataFrame(areaPages)
    save.to_csv('link.csv',header=False,index=False,encoding='utf-8')


getLinks()

# content = []
# def getContent(URL):
#     html = urlopen("https:"+URL, context=context)
#     bsObj = BeautifulSoup(html, "lxml")
#     namelist = bsObj.body.findAll("table", {"border": "0", "cellpadding": "5"})
#     for name in namelist:
#         content.append(name.get_text())
#
#
#
# def getAllContent():
#     getLinks()
#     for links in areaPages:
#         getContent(links)


