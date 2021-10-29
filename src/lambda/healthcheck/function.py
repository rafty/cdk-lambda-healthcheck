import os
from aws_lambda_powertools import Logger
from services import watch_services
from rsslib import rss_read
from sns_alert import alert_service_status
sns_topic_arn = os.environ['SNS_TOPIC_ARN']
logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    logger.info(event)
    try:

        # TODO: for文をへらす　関数化　itertoolsは使わない

        for region, services in watch_services.items():
            for aws_service, rss in services.items():
                status_items = rss_read(rss)
                if len(status_items):
                    alert_service_status(sns_topic_arn, status_items,
                                         aws_service, region)
                else:
                    logger.info(
                        f'{aws_service} is normal at {region}.')
        return {}

    except Exception as e:
        logger.exception(e)
