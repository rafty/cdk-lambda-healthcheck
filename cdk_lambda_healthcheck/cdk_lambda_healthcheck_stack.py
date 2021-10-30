from aws_cdk import core as cdk
from aws_cdk import aws_lambda
from aws_cdk import aws_sam
from aws_cdk import aws_sns
from aws_cdk import aws_sns_subscriptions
from aws_cdk import aws_events
from aws_cdk import aws_events_targets


class CdkLambdaHealthcheckStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        alert_email = 'yagita.takashi+alert@gmail.com'

        topic_service_alert = aws_sns.Topic(
            scope=self,
            id='ServiceAlertTopic',
            topic_name='service_alert',
            display_name='Service Alert'
        )

        topic_service_alert.add_subscription(
            aws_sns_subscriptions.EmailSubscription(alert_email)
        )

        fn_health_check = aws_lambda.Function(
            scope=self,
            id='HealthCheckFunction',
            function_name='health_check',
            handler='function.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset('src/lambda/healthcheck'),
            timeout=cdk.Duration.seconds(300),
            layers=[
                self.power_tools_layer_version()
            ],
            environment={
                # 'LOG_LEVEL': 'DEBUG',
                'LOG_LEVEL': 'INFO',
                'POWERTOOLS_SERVICE_NAME': 'health_check',
                'SNS_TOPIC_ARN': topic_service_alert.topic_arn
            }
        )

        topic_service_alert.grant_publish(fn_health_check)

        alert_target = aws_events.Rule(
            scope=self,
            id='LambdaAlertRule',
            # schedule=aws_events.Schedule.cron(minute=1),
            schedule=aws_events.Schedule.rate(cdk.Duration.minutes(5))
        )
        input_event = aws_events.RuleTargetInput.from_object(dict(foo="bar"))
        alert_target.add_target(
            target=aws_events_targets.LambdaFunction(
                handler=fn_health_check,
                event=input_event
            )
        )

    def power_tools_layer_version(self) -> aws_lambda.LayerVersion:
        # AWS Lambda PowerTools From Serverless Application Repository
        power_tools_arn = ('arn:aws:serverlessrepo:eu-west-1:'
                           '057560766410:applications/'
                           'aws-lambda-powertools-python-layer')
        power_tools_ver = '1.21.1'

        power_tools = aws_sam.CfnApplication(
            scope=self,
            id='AwsLambdaPowerTools',
            location={
                'applicationId': power_tools_arn,
                'semanticVersion': power_tools_ver
            }
        )

        layer_arn = power_tools.get_att("Outputs.LayerVersionArn").to_string()
        layer_version = aws_lambda.LayerVersion.from_layer_version_arn(
            scope=self,
            id='AWSLambdaPowerToolsARN',
            layer_version_arn=layer_arn
        )
        return layer_version
