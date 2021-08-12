from serpapi import GoogleSearch

class SERP:
    def __init__(self, serpapi_api_key: str):
        self.data = {
            "api_key": serpapi_api_key,
            "tbm": "shop",
            "engine": "google"
        }
    
    def get(self, query: str):
        self.data.update({"q": query})
        res = GoogleSearch(self.data).get_dict()
        self.data.pop("q")
        return res

def process(data: dict) -> dict:
    rt = []
    for result in data["shopping_results"]:
        rt.append(
            {
                "title": result["title"],
                "price": result["extracted_price"],
                "supplier": result["source"],
                "link": result["link"]
            }
        )
    for result in data["inline_shopping_results"]:
        rt.append(
            {
                "title": result["title"],
                "price": result["extracted_price"],
                "supplier": result["source"],
                "link": result["link"]
            }
        )
    return {"extracted": rt}