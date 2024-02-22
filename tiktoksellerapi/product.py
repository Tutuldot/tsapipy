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

class Product:

    def __init__(self):
        api = API()
        self.api = api
        
        

    def getSKU(self,skuids,version="202309"):
       
        payload = json.dumps({"sku_ids": skuids})
        url_path = "/product/" + version + "/inventory/search"

        ts = int(time.time())
        req2 = http_client.HTTPMessage()
        req2.path = url_path
        req2.query = "app_key=" + self.api.getAppKey() + "&timestamp=" + str(ts) + "&shop_cipher=" + self.api.getShopCipher()
        req2.add_header("Content-type", "application/json")
        req2.set_payload(payload)
      
        signature = self.api.cal_sign(req2)
        
        url = self.api.getAPIURL() + url_path
       
        f_url = url + "?app_key=" + self.api.getAppKey() + "&shop_cipher=" + self.api.getShopCipher() + "&timestamp=" + str(ts) + "&sign=" + signature 

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
        

    def getProduct(self,product_id,version="202309"):
        
        # 1729831045943560408
        ts = int(time.time())
        req2 = http_client.HTTPMessage()
        url_path = "/product/" + version + "/products/" + product_id
        req2.path = url_path
        req2.query = "app_key=" + self.api.getAppKey() + "&timestamp=" + str(ts) + "&shop_cipher=" + self.api.getShopCipher() 
        req2.add_header("Content-type", "application/json")
        req2.set_payload("")
        signature = self.api.cal_sign(req2)

        url = self.api.getAPIURL() + url_path
      
        f_url = url + "?app_key="+ self.api.getAppKey() +"&shop_cipher=" + self.api.getShopCipher() + "&timestamp=" + str(ts) + "&sign=" + signature 
     
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

