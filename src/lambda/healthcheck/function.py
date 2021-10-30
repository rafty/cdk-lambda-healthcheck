import os
from datetime import datetime, timezone
from aws_lambda_powertools import Logger
from watch_services import watch_services
from rsslib import extract_service_error
from sns_alert import alert_service_status
from watch_services import flatten

sns_topic_arn = os.environ['SNS_TOPIC_ARN']
logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    logger.debug(event)
    try:
        service_list = flatten(watch_services)
        status_list = extract_service_error(service_list)

        for status in status_list:
            alert_service_status(sns_topic_arn, status)

        return None

    except Exception as e:
        logger.exception(e)
        raise e


if __name__ == '__main__':
    handler({}, {})
