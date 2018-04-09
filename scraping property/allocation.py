# coding=utf-8
import json
from urllib.request import urlopen
import pandas as pd
import ssl

context = ssl._create_unverified_context()
file='property.csv'
data=pd.read_csv(file,encoding='utf-8')
ak="AIzaSyCzs5lAW4ySZZbx02I-BXtUl_kyFkVRdLY"
ak_elevation="AIzaSyBFvx9f55RZTlr3Ycxnr0tRrgI1QbuE8Ac"
ak_nearby="AIzaSyByFPRRZjZQnc8S_YhCjKCzk-OrRLMHFY8"
language="en"
url="https://maps.googleapis.com/maps/api/geocode/json?"
elevationUrl="https://maps.googleapis.com/maps/api/elevation/json?"
nearbyUrl="https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
fileNew='property_location.csv'


def get_lat_lng(address):
    splitAddress=address.split(',')
    newUrl=url+"address="+splitAddress[-1].replace(' ','%20')+"&language="+language+"&region=hk&key="+ak
    # print(newUrl)
    response = urlopen(newUrl,context=context).read().decode('utf-8')
    responseJson = json.loads(response)
    lat = responseJson['results'][0]['geometry']['location']['lat']
    lng = responseJson['results'][0]['geometry']['location']['lng']
    return lat,lng


def get_elevation(lat,lng):
    newUrl=elevationUrl+"locations="+lat+","+lng+"&key="+ak_elevation
    response=urlopen(newUrl,context=context).read().decode('utf-8')
    responseJson=json.loads(response)
    elevation=responseJson['results'][0]['elevation']
    return  elevation

#hospital,school,shopping_mall,restaurant,bus_station
def get_nearby(lat,lng,radius,type):
    newUrl=nearbyUrl+"location="+lat+","+lng+"&radius="+radius+"&type="+type+"&key="+ak_nearby
    response = urlopen(newUrl, context=context).read().decode('utf-8')
    responseJson = json.loads(response)
    nearby=len(responseJson['results'])
    return nearby


def addLocation(data):
    loaction = []
    for i in range(len(data.iloc[:,1])):
        lat,lng=get_lat_lng(data.iloc[i,1])
        loaction.append([lat,lng])
    loactionDataFrame=pd.DataFrame(loaction)
    loactionDataFrame.to_csv(fileNew,encoding='utf-8',mode='a+',index=False)


print(get_nearby('22.3366356','114.1402195',radius='500',type='bus_station'))
# print(get_elevation('22.3366356','114.1402195'))
# addLocation(data)

# https://maps.googleapis.com/maps/api/geocode/json?address=+Aberdeen%20Centre&language=en&region=hk&key=AIzaSyCzs5lAW4ySZZbx02I-BXtUl_kyFkVRdLY
# https://maps.googleapis.com/maps/api/elevation/json?locations=22.3366356,114.1402195&key=AIzaSyBFvx9f55RZTlr3Ycxnr0tRrgI1QbuE8Ac
# https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=22.3366356,114.1402195&radius=1000&type=restaurant&key=AIzaSyByFPRRZjZQnc8S_YhCjKCzk-OrRLMHFY8
