import pandas as pd
import json
import os
import boto3
import io
import logging

logging.basicConfig(
    filename='S3_Functions.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

s3 = boto3.client("s3")

bucket_name = "traffic-data-pipeline"
s3_folder_raw = "raw"
s3_folder_transformed = "transformed"
s3_folder_errors = "errors"


def upload_raw_json_to_s3(data, corridor, Time_ID):
    """
    Uploads a raw JSON object to an S3 bucket.

    :param data: The data to write and upload (serializable to JSON).
    :param corridor: Corridor identifier for the file name.
    :param Time_ID: Time identifier for the file name.
    :param bucket_name: The target S3 bucket.
    :param s3_folder: The folder (key prefix) in the S3 bucket. Default: 'raw'.
    """
    file_name = f"{corridor}_{Time_ID}.json"
    s3_key = f"{s3_folder_raw}/{file_name}"

    # Convert data to JSON string
    json_bytes = json.dumps(data, indent=4).encode("utf-8")

    # Upload to S3
    s3.put_object(Bucket=bucket_name, Key=s3_key,
                  Body=json_bytes, ContentType="application/json")


def upload_invalid_rows_to_s3(invalid_rows):

    file_name = f"{invalid_rows['Corridor'].iloc[0]}_{invalid_rows['Time_ID'].iloc[0]}_invalid_rows.csv"
    s3_key = f"{s3_folder_errors}/{file_name}"

    buffer = io.StringIO()
    invalid_rows.to_csv(buffer, index=False)

    try:
        s3.put_object(Bucket=bucket_name, Key=s3_key,
                      Body=buffer.getvalue(), ContentType="text/csv")
        logging.info(f"Invalid rows uploaded to S3 at {s3_key}.")
    except Exception as e:
        logging.error(f"Error uploading invalid rows to S3: {e}")

    logging.info(f"Invalid rows uploaded to S3 at {s3_key}.")


def upload_out_of_bounds_rows_to_s3(out_of_bounds_rows):
    file_name = f"{out_of_bounds_rows['Corridor'].iloc[0]}_{out_of_bounds_rows['Time_ID'].iloc[0]}_out_of_bounds_rows.csv"
    s3_key = f"{s3_folder_errors}/{file_name}"

    buffer = io.StringIO()
    out_of_bounds_rows.to_csv(buffer, index=False)

    try:
        s3.put_object(Bucket=bucket_name, Key=s3_key,
                      Body=buffer.getvalue(), ContentType="text/csv")
        logging.info(f"Out-of-bounds rows uploaded to S3 at {s3_key}.")
    except Exception as e:
        logging.error(f"Error uploading out-of-bounds rows to S3: {e}")


def upload_transformed_parquet_to_s3(df):
    corridor = df['Corridor'].iloc[0]
    year = df['Year'].iloc[0]
    month = f"{int(df['Month'].iloc[0]):02d}"
    day = f"{int(df['Day'].iloc[0]):02d}"
    hour = f"{int(df['Hour'].iloc[0]):02d}"
    minute = f"{int(df['Minute'].iloc[0]):02d}"

    s3_key = (
        f"{s3_folder_transformed}/"
        f"corridor={corridor}/"
        f"year={year}/"
        f"month={month}/"
        f"day={day}/"
        f"hour={hour}/"
        f"minute={minute}/"
        f"transformed.parquet"
    )
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)

    try:
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=df.to_parquet(
        ), ContentType="application/octet-stream")
        logging.info(f"Transformed parquet uploaded to S3 at {s3_key}.")
    except Exception as e:
        logging.error(f"Error uploading transformed parquet to S3: {e}")
