import requests
import os
from dotenv import load_dotenv
from datetime import datetime

Time_Start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"Time Start: {Time_Start}")
load_dotenv()

API_Key = os.getenv("TomTom_API_Key")


Base_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?"

params = {
    "key": API_Key,
    "point": "40.7128,-74.0060",
    "unit": "MPH"
}

response = requests.get(Base_URL, params=params)

data = response.json()

print(data["flowSegmentData"]["currentSpeed"])
