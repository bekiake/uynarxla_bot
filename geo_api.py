import requests
from environs import Env


env = Env()
env.read_env()

def get_geodata(lat, lon):
    api_key = env.str("GEO_API_KEY")
    url = "https://catalog.api.2gis.com/3.0/items/geocode"
    params = {
        "lat": lat,  
        "lon": lon,  
        "fields": "items.point",  
        "key": api_key
    }


    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get('result').get('items')[1].get('full_name')
    else:
        return None
