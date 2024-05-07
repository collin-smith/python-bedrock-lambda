from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
        aws_iam as iam,
        Duration,
    aws_apigateway as apigw
)
from constructs import Construct

class PythonBedrockLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        model_id = "anthropic.claude-3-opus-20240229-v1:0"
        #foundation-model/anthropic.claude-v2
        #foundation-model/anthropic.claude-3-sonnet-20240229-v1:0
        #foundation-model/anthropic.claude-3-opus-20240229-v1:0


               #add policy to invoke bedrock model
        invoke_model_policy = iam.Policy(self, "InvokeModelPolicy",
            statements=[
                iam.PolicyStatement(
                    actions=["bedrock:InvokeModel"],
                    resources=[f"arn:aws:bedrock:{self.region}::foundation-model/anthropic.claude-3-opus-20240229-v1:0"]
                )
            ]
        )

        # Create the Lambda function and attach the layer
        lambda_function = _lambda.Function(self, "MyFunction",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="index.handler",
            code=_lambda.Code.from_asset("./genai_function"),
           # layers=[layer],
            timeout=Duration.seconds(30)
            )

        invoke_model_policy.attach_to_role(lambda_function.role)


         #create api gateway
        api = apigw.RestApi(self, "BedrockApi",)

        #create a new resource
        text_gen_resource = api.root.add_resource("genai")
        text_gen_resource.add_method("POST", apigw.LambdaIntegration(lambda_function))
