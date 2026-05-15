import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

import logging

# Configure logging
logging.basicConfig(
    filename='TestAPI.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

logging.info('Script started.')


Time_Start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
Time_ID = datetime.now().strftime('%Y%m%d%H%M')

load_dotenv()
API_Key = os.getenv("TomTom_API_Key")
Time_ID = datetime.now().strftime('%Y%m%d%H%M')

Base_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?"

params = {
    "key": API_Key,
    "point": "40.7128,-74.0060",
    "unit": "MPH"
}

response = requests.get(Base_URL, params=params)

data = response.json()

print(Time_ID)
