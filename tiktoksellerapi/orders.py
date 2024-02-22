import requests
from http import client as http_client
import time
import json
from tiktoksellerapi.api import API

class Orders:

    def __init__(self):
        api = API()
        self.api = api
   
        

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
    

        url = self.api.getAPIURL() + "/order/" + version +"/orders/search"
      

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
      
