import hashlib
import hmac
import io
import time
import urllib.parse
from typing import Any, Tuple
from http import client as http_client
import requests
import json
from math import radians, cos, sin, asin, sqrt
from dotenv import load_dotenv
import os
from tiktoksellerapi.api import API

class Orders:

    def __init__(self):
        api = API()
        self.api = api
        self.apiUrl = "https://open-api.tiktokglobalshop.com"
        

    def getOrders(self,skuids,version="202309",page_size = 10):
        
        payload = json.dumps({})

        # sign generation

        ts = int(time.time())
        req2 = http_client.HTTPMessage()
        req2.path = "/order/"+ version +"/orders/search"
        req2.query = "app_key=" + self.api.getAppKey() + "&page_size=" + str(page_size) + "&timestamp=" + str(ts) + "&shop_cipher="  + self.api.getShopCipher()
        req2.add_header("Content-type", "application/json")
        req2.set_payload(payload)
        signature = self.api.cal_sign(req2)
    

        url = self.apiUrl + "/order/" + version +"/orders/search"
        params = {
            "app_key": self.api.getAppKey(),
            "shop_cipher" : self.api.getShopCipher(),
            "sku_ids": skuids,
            "sign": signature,
            "timestamp": str(ts)
        }

        f_url = url + "?app_key=" + self.api.getAppKey() +"&page_size="+ str(page_size) + "&shop_cipher=" + self.api.getShopCipher() + "&timestamp=" + str(ts) + "&sign=" + signature 

        response = requests.request("POST",f_url,data=payload,headers = self.api.generate_headers())
        # Check the response status code
        data = []
        if response.status_code == 200:
            # Do something with the response
            data = response.json()
        else:
            # Handle the error
            print("Error: " + response.text)

        return data
      
