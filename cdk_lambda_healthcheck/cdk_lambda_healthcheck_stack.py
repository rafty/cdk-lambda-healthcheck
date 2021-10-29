from aws_cdk import core as cdk
from aws_cdk import aws_lambda
from aws_cdk import aws_sam


class CdkLambdaHealthcheckStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        fn_health_check = aws_lambda.Function(
            scope=self,
            id='HealthCheckFunction',
            function_name='health_check',
            handler='function.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset('src/lambda/healthcheck'),
            layers=[
                self.power_tools_layer_version()
            ],
            environment={
                'LOG_LEVEL': 'DEBUG',
                'POWERTOOLS_SERVICE_NAME': 'health_check'
            }
        )

    def power_tools_layer_version(self) -> aws_lambda.LayerVersion:
        # From Serverless Application Repository
        power_tools_arn = (
            'arn:aws:serverlessrepo:eu-west-1:'
            '057560766410:applications/'
            'aws-lambda-powertools-python-layer')
        power_tools_ver = '1.21.1'

        power_tools = aws_sam.CfnApplication(
            self,
            'AwsLambdaPowerTools',
            location={
                'applicationId': power_tools_arn,
                'semanticVersion': power_tools_ver
            },
        )

        layer_arn = power_tools.get_att("Outputs.LayerVersionArn").to_string()
        layer_version = aws_lambda.LayerVersion.from_layer_version_arn(
            self,
            'AWSLambdaPowerToolsARN',
            layer_arn
        )
        return layer_version
