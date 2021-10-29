from datetime import datetime, timezone
from aws_lambda_powertools import Logger
import boto3

logger = Logger(child=True)
sns = boto3.client('sns')


def message_format(item, aws_service, region):
    message = (
        f'AWS Service Error!!\n'
        f'{aws_service} in {region}\n'
        f'UTC:{item["pub_date"].strftime("%Y/%m/%d %H:%M:%S")}\n\n'
        f'MESSAGE:\n{item["description"]}'
    )
    logger.info(message)
    return message


def alert_service_status(topic_arn, items, aws_service, region):
    """
    - Send to CloudWatch Logs
    - CloudWatch Scheduled Events every 5 minutes
    - 5 minutes x 2 minutes = 600 seconds
    - Notify Items within the last 10 minutes
    """

    logger.info('xml: {}'.format(items))

    for item in items:
        delta = datetime.now(timezone.utc) - item['pub_date']

        # if delta.total_seconds() <= 60 * 5 * 2 * 10000000:  # for test
        if delta.total_seconds() <= 60 * 5 * 2:
            message = message_format(item, aws_service, region)
            sns.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject='Alert! AWS Service Error. {} in {}'.format(
                    aws_service, region))
            logger.info('Message published: {} in {}'.format(
                aws_service, region))
