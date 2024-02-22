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
    #print("app :" + input_str)
    return generate_sha256(input_str, secret)


def generate_sha256(input_str: str, secret: str) -> str:


    # encode the digest byte stream in hexadecimal and use sha256 to generate sign with salt(secret)
    h = hmac.new(bytes(secret, 'utf-8'), msg=bytes(input_str, 'utf-8'), digestmod=hashlib.sha256)

    return h.hexdigest()


def get_all_product_list(self):
    secret_key = "e3af7bf6e342236e7422c491e417d6a1c0a9ef07"
    headers = {
    'x-tts-access-token': 'ROW_9BV4eQAAAAAIAnt06Rs72wGgf6fjXxs7fHqUFvgihDRdTFH8GjesuwUeRUFEeOxBNAfk_fSJreRwBC_YQ3tF9NO6V8BGH-YHI-Vl7-vrtTwRmzMaubtnTWCrG4sM28hold1VVZ_U8L2GOMiFWlx0uhxcw9-C4SbWEIhnh0obfun9GPgI5NULWw'
        ,'Content-Type': 'application/json'
    }

    # https://open-api.tiktokglobalshop.com/product/202312/products/search?app_key=123abc&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1625484268


    ts = int(time.time())
    req2 = http_client.HTTPMessage()
    req2.path = "/product/202312/products/search"
    req2.query = "app_key=6b57ikn775gaj&timestamp=" + str(ts) + "&page_size=100&shop_cipher=ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr&version=202312" 
    req2.add_header("Content-type", "application/json")
    req2.set_payload("")

    secret_key = "e3af7bf6e342236e7422c491e417d6a1c0a9ef07"
    signature = cal_sign(req2, secret_key)
    print("Signature:", signature)

    url = "https://open-api.tiktokglobalshop.com/product/202312/products/search"
    params = {
        "app_key": "6b57ikn775gaj",
        "page_size" : 20,
        "shop_cipher" : "ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr",
        "sign": signature,
        "timestamp": str(ts),
        "version" : 202312
    }

    f_url = url + "?app_key=6b57ikn775gaj&page_size=100&shop_cipher=ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr&timestamp=" + str(ts) + "&sign=" + signature  + "&version=202312"
    print(f_url)
    response = requests.post(f_url ,headers=headers)
    # Check the response status code
    data = []
    if response.status_code == 200:
        # Do something with the response
        data = response.json()
    else:
        # Handle the error
        print("Error: " + response.text)

    d = data['data']['products']
    final_products = []
    for j in d:
        title = j['title']
        id = j['id']
        res = get_product_details(id)
        #print("Title: {} ID: {}".format(title,id))
        final_products.append(res)

    with open('output.json', 'w') as f:
    # Use the dump() method to write the list to the file in JSON format
        json.dump(final_products, f)
    print("done")


def get_product_details(product_id:str):
    secret_key = "e3af7bf6e342236e7422c491e417d6a1c0a9ef07"
    headers = {
    'x-tts-access-token': 'ROW_9BV4eQAAAAAIAnt06Rs72wGgf6fjXxs7fHqUFvgihDRdTFH8GjesuwUeRUFEeOxBNAfk_fSJreRwBC_YQ3tF9NO6V8BGH-YHI-Vl7-vrtTwRmzMaubtnTWCrG4sM28hold1VVZ_U8L2GOMiFWlx0uhxcw9-C4SbWEIhnh0obfun9GPgI5NULWw'
        ,'Content-Type': 'application/json'
    }


    ts = int(time.time())
    req2 = http_client.HTTPMessage()
    req2.path = "/product/202309/products/1729831045943560408"
    req2.query = "app_key=6b57ikn775gaj&timestamp=" + str(ts) + "&shop_cipher=ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr" 
    req2.add_header("Content-type", "application/json")
    req2.set_payload("")
    secret_key = "e3af7bf6e342236e7422c491e417d6a1c0a9ef07"
    signature = cal_sign(req2, secret_key)
    

    url = "https://open-api.tiktokglobalshop.com/product/202309/products/1729831045943560408"
    params = {
        "app_key": "6b57ikn775gaj",
        "shop_cipher" : "ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr",
        "sku_ids": ['1729887427421964504','1729887427421964504'],
        "sign": signature,
        "timestamp": str(ts)
    }

    f_url = url + "?app_key=6b57ikn775gaj&shop_cipher=ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr&timestamp=" + str(ts) + "&sign=" + signature 
    

    response = requests.request("GET",f_url, headers = headers)
    # Check the response status code
    data = []
    if response.status_code == 200:
        # Do something with the response
        data = response.json()
    else:
        # Handle the error
        print("Error: " + response.text)
    
    base_rec = []

    p = data['data']
    title = p['title']
    status = p['status']
    description = p['description']
    product_category = ""
   
    # get the product category
    for cc in p['category_chains']:
        if cc['is_leaf']:
            product_category = cc['local_name']

    skus = p['skus']

    #create entry for destination

    for sku in skus:
        
        product_sku = sku['id']
        product_quantity = 0
        product_price = sku['price']['sale_price']
        product_currency = sku['price']['currency']
        product_sub_category_name = ""
        product_sub_category_image = ""
        for sa in sku['sales_attributes']:
            if sa['name'] == 'Color':
                product_sub_category_name = sa['value_name']
                product_sub_category_image = sa['sku_img']

        
        #calculate inventory from all warehouse
        for inv in sku['inventory']:
            product_quantity += inv['quantity']

        prd = {"sku":product_sku
        , "name":title
        , "category": product_category
        , "qty" : product_quantity
        , "price": product_price
        , "currency" : product_currency
        , "sub_category_name": product_sub_category_name
       # , 'sub_category_image': product_sub_category_image
        }
        
        return prd
        
   
    



get_all_product_list()
