import pandas as pd
import json
import os
import Transform_Functions as tf
from Load_Functions import load_Local_transformed_Parquet
from pathlib import Path
import logging
import shutil

raw_data_path = "C:/GitRepos/Traffic-Project/Data/Raw"
archive_path = "C:/GitRepos/Traffic-Project/Data/Archive"


def Transform_Data(df):
    df = tf.change_data_type(df)
    df = tf.add_date_time_columns(df)
    df = tf.check_for_nulls(df)
    df = tf.filter_out_of_bounds_rows(df)
    df = tf.add_metrics(df)
    df = tf.add_congestion_category(df)
    return df


def process_raw_data():
    logging.info("Transforming data.")
    for file in Path(raw_data_path).glob("*.json"):
        df = pd.read_json(file)
        df = Transform_Data(df)
        corridor = df['Corridor'].iloc[0]
        time_id = df['Time_ID'].iloc[0]
        load_Local_transformed_Parquet(df, corridor, time_id)
        logging.info(
            f"Data transformed successfully for {corridor} at {time_id}.")
        shutil.move(file, Path(archive_path) / file.name)
        logging.info(
            f"Raw data archived successfully for {corridor} at {time_id}.")

    logging.info("All data transformed successfully.")
