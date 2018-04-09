# coding=utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import pandas as pd

saveFile = "property.csv"
dataFile = "link.csv"


def saveData(url):
    context = ssl._create_unverified_context()
    html = urlopen("https:"+url, context=context)
    print(url)
    bsObj = BeautifulSoup(html, "lxml")
    namelist = bsObj.body.findAll("table", {"border": "0", "cellpadding": "5"})[0]
    rows = namelist.findAll("tr")
    csvData=[]
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td','th']):
            if cell.find(['br']):
                split=cell.get_text(' ', strip=True).split(' ')
                for i in range(0,len(split)):
                    csvRow.append(split[i])
            else:
                csvRow.append(cell.get_text())
        csvData.append(csvRow)
    save=pd.DataFrame(csvData)
    save1=save[1:-1]
    # print(save1.dropna(axis=1,how='all'))
    save1.dropna(axis=1, how='all').to_csv(saveFile,encoding='utf-8',mode='a+',index=False)

def getData():
    data = pd.read_csv(dataFile, encoding='utf-8',names=['links'])
    for i in range(0,len(data['links'])-1):
        url=data.iloc[i,0]
        saveData(url)



# getData()
saveData("//transactions.gohome.com.hk/records/Mei-Foo/Mei-Foo-Sun-Chuen/en/?Page=5")