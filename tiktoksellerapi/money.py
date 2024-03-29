import requests
from http import client as http_client
import time
import json
from tiktoksellerapi.api import API

class Money:

    def __init__(self):
        api = API()
        self.api = api
        
        

    def getStatements(self,skuids,version="202309"):
       
   
        ts = int(time.time())
        req2 = http_client.HTTPMessage()
        req2.path = "/finance/"+version+"/statements"
        req2.query = "app_key=" + self.api.getAppKey() + "&sort_field=statement_time&payment_status=PROCESSING&timestamp=" + str(ts) + "&shop_cipher=" + self.api.getShopCipher()
        req2.add_header("Content-type", "application/json")
        req2.set_payload("")

        signature = self.api.cal_sign(req2)
    

        url = self.api.getAPIURL() + "/finance/" + version + "/statements"
      
        f_url = url + "?app_key=" + self.api.getAppKey() + "&sort_field=statement_time&payment_status=PROCESSING&shop_cipher=" + self.api.getShopCipher() + "&timestamp=" + str(ts) + "&sign=" + signature 

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

    def getPayments(self,skuids,version="202309"):
        

        ts = int(time.time())
        req2 = http_client.HTTPMessage()
        req2.path = "/finance/" + version + "/payments"
        req2.query = "app_key=" + self.api.getAppKey() + "&sort_field=create_time&timestamp=" + str(ts) + "&shop_cipher=" + self.api.getShopCipher() 
        req2.add_header("Content-type", "application/json")
        req2.set_payload("")
      
        signature = self.api.cal_sign(req2)


        url = self.api.getAPIURL() + "/finance/" + version + "/payments"
       
        f_url = url + "?app_key=" + self.api.getAppKey() + "&sort_field=create_time&shop_cipher=" + self.api.getShopCipher() + "&timestamp=" + str(ts) + "&sign=" + signature 


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




