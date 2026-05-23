import boto3
import json

s3 = boto3.client("s3")

bucket_name = "traffic-data-pipeline"
s3_folder_raw = "raw"


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
