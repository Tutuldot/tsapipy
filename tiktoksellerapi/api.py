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


"""
This class holds all API request methods
"""
class API:
    def __init__(self):
        load_dotenv()  # load environment variables from .env file
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.secret_key = os.getenv("SECRET_KEY")
        self.app_key = os.getenv("APP_KEY")
        self.refresh_token = os.getenv("REFRESH_TOKEN")
        self.shop_cipher = os.getenv("SHOP_CIPHER")
    
    def getAPIURL(self):
        return "https://open-api.tiktokglobalshop.com"

    def getShopCipher(self):
        return self.shop_cipher

    def getSecretKey(self):
        return self.secret_key
    
    def getAccessToken(self):
        return self.access_token

    def getAppKey(self):
        return self.app_key

    def getKeys():
        """
        :return: secret_key, access_token, app_key, shop_cipher
        """
        return self.secret_key, self.access_token, self.app_key, self.shop_cipher
    

    def checkenv(self):
        res = True
        if self.access_token is None or self.secret_key is None or self.app_key is None:
            res = False
        return res

    def cal_sign(self, req: http_client.HTTPMessage) -> str:
        """
        This function is used for creating signiture for request
        :param req: http_client.HTTPMessage object
        :return: String of the signiture
        """

        secret = self.secret_key
        queries = urllib.parse.parse_qs(req.query)

        # extract all query parameters excluding sign and access_token
        keys = [k for k in queries.keys() if k != "sign" and k != "access_token"]
        keys.sort()

        # Concatenate all the parameters in the format of {key}{value}
        input_str = ""
        
        for key in keys:
            input_str += key + queries[key][0]

        # append the request path
        
        input_str = req.path + input_str
        
        # if the request header Content-type is not multipart/form-data, append body to the end
        content_type = req.get("Content-type", "")
        if content_type != "multipart/form-data":
            body = req.get_payload()
            input_str += body

        
        # wrap the string generated in step 5 with the App secret
        input_str = secret + input_str + secret
    
        return self.generate_sha256(input_str)


    def generate_sha256(self,input_str: str) -> str:

        secret = self.secret_key
        # encode the digest byte stream in hexadecimal and use sha256 to generate sign with salt(secret)
        h = hmac.new(bytes(secret, 'utf-8'), msg=bytes(input_str, 'utf-8'), digestmod=hashlib.sha256)

        return h.hexdigest()

    def generate_headers(self):
        return {
    'x-tts-access-token': self.access_token
        ,'Content-Type': 'application/json'    
    }

    def perform_refresh_token(self):
        return True


