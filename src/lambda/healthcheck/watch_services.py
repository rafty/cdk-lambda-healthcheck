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
