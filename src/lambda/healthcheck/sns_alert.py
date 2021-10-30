from aws_lambda_powertools import Logger
import boto3

logger = Logger(child=True)
sns = boto3.client('sns')


def message_format(status):
    time = status["pacific_time"].strftime("%Y/%m/%d %H:%M:%S")

    message = (
        'AWS Service Error!!\n'
        f'{status["service"]} in {status["region"]}\n'
        f'UTC:{time}\n'
        '------'
        f'MESSAGE:\n{status["description"]}'
    )

    subject = f'Alert! AWS Service Error. {status["service"]} in {status["region"]}'
    return message, subject


def alert_service_status(topic_arn, status):
    message, subject = message_format(status)

    if status['description'] != 'Normal':
        # TODO hoge
        # sns.publish(
        #     TopicArn=topic_arn,
        #     Message=message,
        #     Subject=subject)
        logger.info(f'Message published: \n{message} \n Subject: {subject}')
    else:
        logger.info(f'Service: {status["service"]}, Region: {status["region"]}, Status: {status["description"]}')
