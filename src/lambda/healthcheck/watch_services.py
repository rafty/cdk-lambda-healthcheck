from aws_lambda_powertools import Logger

logger = Logger(child=True)

# AWS Service Health Dashboard RSS
# https://status.aws.amazon.com/


watch_services = {
    "ap-northeast-1": {
        "AWS Lambda": 'https://status.aws.amazon.com/rss/lambda-ap-northeast-1.rss',
        "Transfer for SFTP": 'https://status.aws.amazon.com/rss/transfer-ap-northeast-1.rss',
        "EC2": "https://status.aws.amazon.com/rss/ec2-ap-northeast-1.rss",
        'CloudWatch': 'https://status.aws.amazon.com/rss/cloudwatch-ap-northeast-1.rss'
    },
    "us-east-1": {
        "EC2": 'https://status.aws.amazon.com/rss/ec2-us-east-1.rss'
    },
    "global": {
        "Console": "https://status.aws.amazon.com/rss/management-console.rss",
        "Route53": "https://status.aws.amazon.com/rss/route53.rss"
    }
}


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
            service_list.append(
                dict(region=region, service=service, rss=rss))
    return service_list
