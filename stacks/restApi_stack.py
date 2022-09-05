from aws_cdk.aws_apigateway import MethodResponse, TokenAuthorizer, IntegrationResponse, RequestValidatorOptions, \
    RequestValidator
from aws_cdk.core import CfnOutput, Stack
from constructs import Construct
import os
from aws_cdk import aws_lambda as lambda_
from aws_cdk.aws_apigateway import PassthroughBehavior, RestApi, LambdaIntegration, AuthorizationType

DIRNAME = os.path.dirname(__file__)
class RestApiStack(Stack):
   def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Create the Lambda function to handle the API
        lambda_backend_fn = lambda_.Function(
            self, "BackendLambdaFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="main.lambda_handler",
            code=lambda_.Code.from_asset(os.path.join(DIRNAME, "../lambda_backend")),

        )

        # Create the Lambda authorizer function
        lambda_authorizer_fn = lambda_.Function(
              self, "lambdaAuthorizerFn",
              runtime=lambda_.Runtime.PYTHON_3_9,
              handler="auth.lambda_handler",
              code=lambda_.Code.from_asset(os.path.join(DIRNAME, "../lambdaAuthorizer")),
        )

        # Lambda Backend Integraion
        lambdaBackendIntegration = LambdaIntegration(lambda_backend_fn,
                                                        proxy=False,
                                                        passthrough_behavior=PassthroughBehavior.WHEN_NO_TEMPLATES,
                                                         request_templates={
                                                         "application/json": "#set($allParams = $input.params()) { \"body-json\" : $input.json('$'), \"params\" : { #foreach($type in $allParams.keySet()) #set($params = $allParams.get($type)) \"$type\" : { #foreach($paramName in $params.keySet()) \"$paramName\" : \"$util.escapeJavaScript($params.get($paramName))\" #if($foreach.hasNext),#end #end } #if($foreach.hasNext),#end #end }, \"stage-variables\" : { #foreach($key in $stageVariables.keySet()) \"$key\" : \"$util.escapeJavaScript($stageVariables.get($key))\" #if($foreach.hasNext),#end #end }, \"context\" : { \"http-method\" : \"$context.httpMethod\", \"stage\" : \"$context.stage\" } }"
                                                         },
                                                        integration_responses=[IntegrationResponse(status_code="200")]
                                                     )


        # New Authorizer based on your existing Lambda
        lambda_authorizer = TokenAuthorizer(self, "myAuthorizer", handler=lambda_authorizer_fn)
        rest_api = RestApi(self, "RestApi")

        # it's an request validator settings
        request_validator = RequestValidator(self, "QueryPathValidator",
                                                        rest_api=rest_api,
                                                        # the properties below are optional
                                                        request_validator_name="queryPathValidator",
                                                        validate_request_body=False,
                                                        validate_request_parameters=True
                                                        )

        # All API's
        # Get user
        getUser = rest_api.root.add_resource('user').add_resource('{value}')
        getUser.add_method('GET',
                            integration=lambdaBackendIntegration,
                            request_parameters={"method.request.path.value": True},
                            request_validator=request_validator,
                            authorization_type=AuthorizationType.CUSTOM,
                            authorizer=lambda_authorizer,
                            method_responses=[MethodResponse(status_code="200")]
                            )
        # Add user
        addUser = rest_api.root.get_resource('user')
        addUser.add_method('POST',
                        integration=lambdaBackendIntegration,
                        request_parameters={"method.request.querystring.username": True},
                        request_validator=request_validator,
                        authorization_type=AuthorizationType.CUSTOM,
                        authorizer=lambda_authorizer,
                        method_responses=[MethodResponse(status_code="200")]
                       )

        CfnOutput(self, "APIURL",
               value=f"https://{rest_api.rest_api_id}.execute-api.us-west-1.amazonaws.com/prod/"
        )
