import pandas as pd
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from Load_Functions import load_Local_raw_json
import logging
import time


def Run_Extraction():
    Start_Time = datetime.now()
    Time_ID = datetime.now().strftime('%Y%m%d%H%M')

    logging.basicConfig(
        filename='Tom_Tom_API.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s'
    )

    logging.info('Script started.')

    load_dotenv()
    # API SET UP
    API_Key = os.getenv("TomTom_API_Key")
    Base_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?"

    # LOAD INPUT VIA POINTS
    corridors = pd.read_csv(
        r"C:\GitRepos\Traffic-Project\Config\Corridor_Data_v2.csv")

    # START OF LOOP. FIRST ARRANGED BY CORRIDOR AND THEN BY POINT. EXAMPLE "I-71 HAS 14 POINTS TO RUN THROUGH"
    for corridor_name, corridor_df in corridors.groupby("Corridor"):
        all_results = []
        logging.info(f"Starting corridor: {corridor_name}")
        print(f"\nProcessing corridor: {corridor_name}")

        for _, row in corridor_df.iterrows():
            lat = row["Latitude"]
            lon = row["Longitude"]
            params = {  # LOAD THE LAT AND LON FOR THIS API CALL
                "key": API_Key,
                "point": f"{lat},{lon}",
                "unit": "MPH",
            }

            # SET SIMPLE RETRY LOGIC. I CAN ADD SPECIFIC RETRIES LATER BASED ON THE ERROR
            for attempt in range(2):
                try:
                    response = requests.get(
                        Base_URL, params=params, timeout=20)
                    response.raise_for_status()
                    data = response.json()
                    # ADD META DATA TO THE RESPONSE DATA
                    all_results.append({
                        "Corridor": row["Corridor"],
                        "Point_ID": row["Point_ID"],
                        "Time_ID": Time_ID,
                        "Current_Speed": data["flowSegmentData"]["currentSpeed"],
                        "Free_Flow_Speed": data["flowSegmentData"]["freeFlowSpeed"],
                        "Current_Travel_Time": data["flowSegmentData"]["currentTravelTime"],
                        "Free_Flow_Travel_Time": data["flowSegmentData"]["freeFlowTravelTime"],
                        "Confidence": data["flowSegmentData"]["confidence"],
                        "Road_Closure": data["flowSegmentData"]["roadClosure"],
                    })
                    print(f"  OK: {lat},{lon}")
                    break  # Exit the retry loop after a successful request
                except requests.RequestException as e:
                    if attempt == 0:
                        time.sleep(0.2)  # Wait before retrying
                        continue
                    print(f"  ERROR: {lat},{lon} -> {e}")
                    logging.error(
                        f"Failed to process {corridor_name}: {e}")
        logging.info(
            f"Received {len(all_results)} records for {corridor_name}")

    # SAVE LOCAL JSON FILE LOCALLY. THIS WILL BE UPDATED TO SAVE TO AN S3 BUCKET
        try:
            load_Local_raw_json(all_results, corridor_name, Time_ID)
            logging.info(f"Saved raw file for : {corridor_name}")
        except Exception as e:
            logging.error(f"Failed to save raw file for {corridor_name}: {e}")

    End_Time = datetime.now()
    Run_Time = (End_Time - Start_Time).total_seconds()

    logging.info(f"Pipeline finished")
    logging.info(f"Runtime: {Run_Time:.2f} seconds")


Run_Extraction()
