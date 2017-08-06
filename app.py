#!/usr/bin/env python

import urllib
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import os
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
intent_name="string"
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print("after json.dumps",res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("action") != "property_search":
        return {}
    global city_names
    global QR
    global intent_name
    intent_name=processIntentName(req)
    city_names=processlocation(req)
    property_type=processPropertyType(req)
    maximum_value=processMaximum(req)
    #baseurl = "https://aarz.pk/bot/index.php?city_name="+city_names+"&sector_name="+sector_names+"&minPrice="+maximum_value+"&type="+property_type+"&LatestProperties="+latest+"&UnitArea="+area_property+"&Unit="+unit_property+"&school="+school+"&airport="+airport+"&transport="+transport+"&security="+security+"&shopping_mall="+malls+"&fuel="+fuel
    #baseurl="https://www.aarz.pk/search/bot?postedBy=searchPage&view=&city_s="+city_names+"&price_min="+maximum_value+"&price_max=0estate_agent=&purpose=Sell&property_type="+property_type

    baseurl="https://www.aarz.pk/search/bot?postedBy=searchPage&view=&city_s="+city_names+"&type="+property_type+"&price_max="+maximum_value
    #print("city:",city_names)
    print("url is:",baseurl)
    result = urllib.request.urlopen(baseurl).read()
    #print('result of url:', result)
    data = json.loads(result)
    #print('data:', data)
    res2=json_to_text(data)
    print('res2:',res2)
    return res2

def processIntentName(req):
    result = req.get("result")
    parameters = result.get("metadata")
    intent = parameters.get("intentName")
    return intent

def processlocation(req):
    global city
    result = req.get("result")
    parameters = result.get("parameters")
    cityNames = parameters.get("location")
    city = cityNames.get("city")
    #print("city data:", city)
    #print("city:", city)

    return city


def processMaximum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    maximum = parameters.get("PriceRange")
    return maximum

def processMinimum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    min_price = parameters.get("min_price")
    return min_price

def processPropertyType(req):
    result = req.get("result")
    parameters = result.get("parameters")
    propertyType = parameters.get("PropertyType")
    return propertyType


def processProjectName(req):
    result = req.get("result")
    parameters = result.get("parameters")
    project_name = parameters.get("ProjectName")
    return project_name 


def json_to_text(data):
     i=0
     length=len(data)
     speech_data = "Here are some properties with your choice. We have total of "+str(length)+" records of your interest in city  "+city+"."
     text_data = "Here are some properties with your choice. We have total of "+str(length)+" records of your interest in city  "+city+"."
     row_id=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
     row_title=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
     row_location=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
     row_price=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
     row_slug=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
     row_number=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
     row_image=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
     row_city=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
     while (i <length):
        row_id[i]=data[i]['property_id']
        row_title[i]=data[i]['title']
        row_location[i]=data[i]['address']
        row_price[i]=data[i]['price']
        row_slug[i]=data[i]['slug']
        row_number[i]=data[i]['number']
        row_image[i]=data[i]['image']
        row_city[i]=data[i]['city_name']
        speech_data_parts="Here is record " + str(i+1) +":"+ row_title[i]+" in city "+row_city[i] + " price is "+ str(row_price[i]) + "."
        speech_data = speech_data + speech_data_parts
        text_data_parts ="Here is record " + str(i+1) +":"+ row_title[i]+" in city "+row_city[i] + " price is "+ str(row_price[i])+ ". For Info about this contact at number "+str(row_number[i]) + "."
        text_data = text_data + text_data_parts	
        i+=1
     #print('speech Data',speech_data)
     #print('Text Data',text_data)
     return {
        "speech": text_data,
        "displayText": text_data,
        "data": {},
        "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
