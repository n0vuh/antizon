import requests
import json 
from .schemes import amznProduct

params = {
  'api_key': '66A685895A2F46D0BC7CF613DC35AEB4',
  'type': 'product',
  'amazon_domain': 'amazon.com',
  'asin': 'B073JYC4XM',
  'output': 'json',
  'device': 'desktop',
  'include_html': 'false',
  'language': 'en_US'
}

class AMZN:
    def __init__(self, rainforest_api_key: str):
        self.params = {
            "api_key": rainforest_api_key,
            "type": "offers",
            "amazon_domain": "amazon.com",
            "output": "json",
            "include_html": "false",
            "language": "en_US"
        }

    def get_item(self, asin: str) -> amznProduct:
        """Returns item metadata from ASIN"""
        self.params.update({"asin": asin})
        with requests.get("https://api.rainforestapi.com/request", self.params, stream=True) as res:
            self.params.pop("asin")
            content = res.json()
            info = content["request_info"]
            # print(content)
            if info["success"] == True:
                product = content["product"]
                offers = content["offers"]
                return amznProduct(product["title"], offers[0]["price"]["value"], asin)
            else:
                return {"message": info["message"]}

