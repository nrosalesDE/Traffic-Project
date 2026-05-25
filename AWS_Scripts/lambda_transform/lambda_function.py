import Transform
import pandas as pd
import S3_Functions_transform


def lambda_handler(event, context):
    record = event['Records'][0]
    s3_bucket = record['s3']['bucket']['name']
    s3_key = record['s3']['object']['key']
    df = pd.read_json(f"s3://{s3_bucket}/{s3_key}")
    df = Transform.Transform_Data(df)
    S3_Functions_transform.upload_transformed_parquet_to_s3(df)
    return {
        "statusCode": 200,
        "body": "Transform completed"
    }
