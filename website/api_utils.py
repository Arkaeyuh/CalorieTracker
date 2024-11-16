import requests
from flask import current_app

def search_food_item(query):
    #TODO: replace the api-key with an environmental var before comitting
    api_key = current_app.config['FOODDATA_API_KEY']
    base_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "query": query,
        "api_key": api_key,
        "pageSize": 1
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['foods']:
            return data['foods'][0]
    return None

def get_nutrient_info(fdc_id):
    api_key = current_app.config['FOODDATA_API_KEY']
    base_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
    params = {
        "api_key" : api_key
    }
    
    response = requests.get(base_url, params=params)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    return None

