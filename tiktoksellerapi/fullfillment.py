import requests
from http import client as http_client
import time
import json
from tiktoksellerapi.api import API

class Fullfillment:

    def __init__(self):
        api = API()
        self.api = api
   
        

    def getPackagesByCreateDate(self,startdate,enddate = None,version="202309",page_size = 10):

        url_path = "/fulfillment/"+ version +"/packages/search"
        
        ts = int(time.time())
        req2 = http_client.HTTPMessage()
        req2.path = url_path
        req2.query = "app_key=" + self.api.getAppKey() + "&page_size=20&timestamp=" + str(ts) + "&shop_cipher=" + self.api.getShopCipher() 
        req2.add_header("Content-type", "application/json")
        req2.set_payload("")
      
        signature = self.api.cal_sign(req2)


        url = self.api.getAPIURL() + url_path
       
        f_url = url + "?app_key=" + self.api.getAppKey() + "&page_size=20&shop_cipher=" + self.api.getShopCipher() + "&timestamp=" + str(ts) + "&sign=" + signature 


        response = requests.request("GET",f_url, headers = self.api.generate_headers())
        # Check the response status code
        data = []
        if response.status_code == 200:
            # Do something with the response
            data = response.json()
        else:
            # Handle the error
            print("Error: " + response.text)

        return data
      
