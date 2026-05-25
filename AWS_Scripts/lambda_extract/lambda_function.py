import logging

import Tom_Tom_API

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s]: %(message)s",
)

logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    Tom_Tom_API.Run_Extraction()
    return {
        "statusCode": 200,
        "body": "Extract completed"
    }
