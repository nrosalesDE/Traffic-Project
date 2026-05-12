import requests
import os

import os
from dotenv import load_dotenv

load_dotenv()

API_Key = os.getenv("TomTom_API_Key")


Base_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?"

params = {
    "key": API_Key,
    "point": "40.7128,-74.0060",
    "unit": "MPH"
}

response = requests.get(Base_URL, params=params)

print(response.json())
