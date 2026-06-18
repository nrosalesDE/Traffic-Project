import logging

import Tom_Tom_API

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    Tom_Tom_API.Run_Extraction()
    return {
        "statusCode": 200,
        "body": "Extract completed"
    }
