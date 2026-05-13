import pandas as pd
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

Time_Start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

load_dotenv()

API_Key = os.getenv("TomTom_API_Key")

Base_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?"

corridors = pd.read_csv(
    r"C:\GitRepos\Traffic-Project\Config\Corridor_Data_v2.csv")


for corridor_name, corridor_df in corridors.groupby("Corridor"):
    all_results = []
    print(f"\nProcessing corridor: {corridor_name}")
    for _, row in corridor_df.iterrows():
        lat = row["Latitude"]
        lon = row["Longitude"]
        params = {
            "key": API_Key,
            "point": f"{lat},{lon}",
            "unit": "MPH",
        }
        try:
            response = requests.get(Base_URL, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
            all_results.append({
                "Corridor": row["Corridor"],
                "Point_ID": row["Point_ID"],
                "Run_Time": Time_Start,
                "Current_Speed": data["flowSegmentData"]["currentSpeed"],
                "Free_Flow_Speed": data["flowSegmentData"]["freeFlowSpeed"],
                "Current_Travel_Time": data["flowSegmentData"]["currentTravelTime"],
                "Free_Flow_Travel_Time": data["flowSegmentData"]["freeFlowTravelTime"],
                "Confidence": data["flowSegmentData"]["confidence"],
                "Road_Closure": data["flowSegmentData"]["roadClosure"],
            })
            print(f"  OK: {lat},{lon}")
        except requests.RequestException as e:
            print(f"  ERROR: {lat},{lon} -> {e}")
