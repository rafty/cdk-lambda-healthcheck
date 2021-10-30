import os
from datetime import datetime, timezone
from aws_lambda_powertools import Logger
from watch_services import watch_services
from rsslib import rss_read
from sns_alert import alert_service_status

# TODO: enter
# sns_topic_arn = os.environ['SNS_TOPIC_ARN']
logger = Logger()


def flatten(_watch_services):
    # e.g. output
    # [
    #     {
    #         'region': 'ap-northeast-1',
    #         'service': 'AWS Lambda',
    #         'rss': 'https://status.aws.amazon.com/rss/lambda-ap-northeast-1.rss'
    #     },
    #     {
    #         'region': 'ap-northeast-1',
    #         'service': 'Transfer for SFTP',
    #         'rss': 'https://status.aws.amazon.com/rss/transfer-ap-northeast-1.rss'
    #     },
    #     {
    #         'region': 'ap-northeast-1',
    #         'service': 'EC2',
    #         'rss': 'https://status.aws.amazon.com/rss/ec2-ap-northeast-1.rss'
    #     },
    #     {
    #         'region': 'ap-northeast-1',
    #         'service': 'CloudWatch',
    #         'rss': 'https://status.aws.amazon.com/rss/cloudwatch-ap-northeast-1.rss'
    #     },
    #     {
    #         'region': 'us-east-1',
    #         'service': 'EC2',
    #         'rss': 'https://status.aws.amazon.com/rss/ec2-us-east-1.rss'
    #     },
    #     {
    #         'region': 'global',
    #         'service': 'Console',
    #         'rss': 'https://status.aws.amazon.com/rss/management-console.rss'
    #     },
    #     {
    #         'region': 'global',
    #         'service': 'Route53',
    #         'rss': 'https://status.aws.amazon.com/rss/route53.rss'
    #     }
    # ]
    service_list = []
    for region, services in _watch_services.items():
        for service, rss in services.items():
            # service_list.append((region, service, rss))
            service_list.append(dict(region=region, service=service, rss=rss))
    return service_list


def extract_service_error(service_list):
    extracted_status_list = []
    for service in service_list:
        service_error_status_list = rss_read(service.get('rss'), service.get('service'), service.get('region'))

        error_count = 0
        for status in service_error_status_list:
            delta = datetime.now(timezone.utc) - status['pacific_time']
            if delta.total_seconds() <= (5 * 60) * 2:  # 5 min(Polling interval) x 2
                extracted_status_list.append(status)
                error_count += 1

        if not error_count:
            extracted_status_list.append(
                dict(description='Normal',
                     pacific_time=datetime.now(timezone.utc),
                     service=service.get('service'),
                     region=service.get('region')))

    return extracted_status_list


# @logger.inject_lambda_context(log_event=True)
def handler(event, context):
    logger.debug(event)
    try:
        service_list = flatten(watch_services)
        status_list = extract_service_error(service_list)

        for status in status_list:
            alert_service_status("", status)
            # TODO sns_topic_arn

        return None

    except Exception as e:
        logger.exception(e)
        raise e
