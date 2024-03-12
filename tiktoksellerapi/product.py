
import requests
from http import client as http_client
import time
import json
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
        

    def getProductDetails(self,product_id,version="202309"):
        
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
    
    def get_product_details(self, product_id:str,version="202309"):
        ts = int(time.time())
        url_path = "/product/202309/products/" + product_id
        req2 = http_client.HTTPMessage()
        req2.path = url_path
        req2.query = "app_key=" + self.api.getAppKey() + "&timestamp=" + str(ts) + "&shop_cipher=" + self.api.getShopCipher() 
        req2.add_header("Content-type", "application/json")
        req2.set_payload("")
   
        signature = self.api.cal_sign(req2)
        

        url = self.api.getAPIURL() + url_path
        

        f_url = url + "?app_key=" + self.api.getAppKey() + "&shop_cipher=" + self.api.getShopCipher() + "&timestamp=" + str(ts) + "&sign=" + signature 
        
        
        response = requests.request("GET",f_url, headers = self.api.generate_headers())
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
       
        main_images = p['main_images'][0]['urls'][0]
        
        # get the product category
        for cc in p['category_chains']:
            if cc['is_leaf']:
                product_category = cc['local_name']

        skus = p['skus']

        #create entry for destination

        final_skus = []

        for sku in skus:
           
            product_sku = sku['id']
            product_quantity = 0
            product_price = sku['price']['sale_price']
            product_currency = sku['price']['currency']
            product_sub_category_name = ""
            product_sub_category_image = "NCA"
            
            for sa in sku['sales_attributes']:
                    
                if sa['name'] == 'Color':
                    product_sub_category_image = None
                    product_sub_category_name = sa['value_name']

                    product_sub_category_image = main_images
                    if 'sku_img' in sa:
                        product_sub_category_image = sa['sku_img']
                    else:
                        product_sub_category_image = main_images
                else:
                    product_sub_category_image = main_images

                    
                        

                    #print("img: {} ID: {}".format(product_sub_category_image,product_id)) #display log

            
            #calculate inventory from all warehouse
            for inv in sku['inventory']:
                product_quantity += inv['quantity']

            prd = {"sku":product_sku
            ,"product_id": product_id
            , "name":title
            , "category": product_category
            , "qty" : product_quantity
            , "price": product_price
            , "currency" : product_currency
            , "sub_category_name": product_sub_category_name
            , 'sub_category_image': product_sub_category_image
            }
            
            final_skus.append(prd)
        return final_skus

    def get_all_product_list(self, version="202312", write_output = False):
        
        ts = int(time.time())
        req2 = http_client.HTTPMessage()
        req2.path = "/product/202312/products/search"
        req2.query = "app_key=6b57ikn775gaj&timestamp=" + str(ts) + "&page_size=100&shop_cipher=ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr&version=202312" 
        req2.add_header("Content-type", "application/json")
        req2.set_payload("")

        signature = self.api.cal_sign(req2)
    
        
        url = "https://open-api.tiktokglobalshop.com/product/202312/products/search"
        

        f_url = url + "?app_key=6b57ikn775gaj&page_size=100&shop_cipher=ROW_PH68hwAAAADLEA37wZU4K8LufewN_8Gr&timestamp=" + str(ts) + "&sign=" + signature  + "&version=202312"
        
        response = requests.post(f_url ,headers=self.api.generate_headers())
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
            #print("Title: {} ID: {}".format(title,id))
            res = self.get_product_details(id)

            for zz in res:
                final_products.append(zz)
            
            
        if write_output:
            with open('output.json', 'w') as f:
            # Use the dump() method to write the list to the file in JSON format
                json.dump(final_products, f)
            #print("done")

        return final_products
        

