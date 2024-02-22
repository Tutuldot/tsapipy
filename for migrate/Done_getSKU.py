import hashlib
import hmac
import io
import time
import urllib.parse
from typing import Any, Tuple
from http import client as http_client
import requests
import json



def cal_sign(req: http_client.HTTPMessage, secret: str) -> str:
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
  
    return generate_sha256(input_str, secret)


def generate_sha256(input_str: str, secret: str) -> str:


    # encode the digest byte stream in hexadecimal and use sha256 to generate sign with salt(secret)
    h = hmac.new(bytes(secret, 'utf-8'), msg=bytes(input_str, 'utf-8'), digestmod=hashlib.sha256)

    return h.hexdigest()
# https://open-api.tiktokglobalshop.com/authorization/202309/shops?app_key=6b57ikn775gaj&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1625484268
# Example Usage:
ts = int(time.time())
req = http_client.HTTPMessage()
req.path = "/authorization/202309/shops"
req.query = "app_key=6b57ikn775gaj&timestamp=" + str(ts)
req.add_header("Content-type", "application/json")
req.set_payload("{'key':'value'}")

secret_key = "e3af7bf6e342236e7422c491e417d6a1c0a9ef07"
signature = cal_sign(req, secret_key)



#https://open-api.tiktokglobalshop.com/authorization/202309/shops?app_key=6b57ikn775gaj&sign={{sign}}&timestamp={{timestamp}}


url = "https://open-api.tiktokglobalshop.com/authorization/202309/shops"
params = {
    "app_key": "6b57ikn775gaj",
    "sign": signature,
    "timestamp": str(ts)
}


headers = {
  'x-tts-access-token': 'ROW_9BV4eQAAAAAIAnt06Rs72wGgf6fjXxs7fHqUFvgihDRdTFH8GjesuwUeRUFEeOxBNAfk_fSJreRwBC_YQ3tF9NO6V8BGH-YHI-Vl7-vrtTwRmzMaubtnTWCrG4sM28hold1VVZ_U8L2GOMiFWlx0uhxcw9-C4SbWEIhnh0obfun9GPgI5NULWw'
    ,'Content-Type': 'application/json'
    
}




# https://open-api.tiktokglobalshop.com/product/202309/inventory/search?app_key=6b57ikn775gaj&timestamp={{timestamp}}&shop_cipher=ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr
payload = json.dumps({
  "sku_ids": [
    "1729887427421964504"
  ]
})

ts = int(time.time())
req2 = http_client.HTTPMessage()
req2.path = "/product/202309/inventory/search"
req2.query = "app_key=6b57ikn775gaj&timestamp=" + str(ts) + "&shop_cipher=ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr" 
req2.add_header("Content-type", "application/json")
req2.set_payload(payload)
secret_key = "e3af7bf6e342236e7422c491e417d6a1c0a9ef07"
signature = cal_sign(req2, secret_key)
print("Signature:", signature)

url = "https://open-api.tiktokglobalshop.com/product/202309/inventory/search"
params = {
    "app_key": "6b57ikn775gaj",
    "shop_cipher" : "ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr",
    "sku_ids": ['1729887427421964504','1729887427421964504'],
    "sign": signature,
    "timestamp": str(ts)
}

f_url = url + "?app_key=6b57ikn775gaj&shop_cipher=ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr&timestamp=" + str(ts) + "&sign=" + signature 
print(f_url)




response = requests.request("POST",f_url,data=payload,headers = headers)
# Check the response status code
data = []
if response.status_code == 200:
    # Do something with the response
    data = response.json()
else:
    # Handle the error
    print("Error: " + response.text)

print(data)

