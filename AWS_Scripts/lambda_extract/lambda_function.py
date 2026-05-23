import Tom_Tom_API


def lambda_handler(event, context):
    Tom_Tom_API.Run_Extraction()
    return {
        "statusCode": 200,
        "body": "Extract completed"
    }
