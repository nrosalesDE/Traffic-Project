import boto3

s3 = boto3.client("s3")

s3.upload_file(
    r"C:\GitRepos\Traffic-Project\Test Scripts\test.json",
    "traffic-data-pipeline",
    "raw/test.json"
)

print("Upload complete")
