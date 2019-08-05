import os
import sys
import json
import boto3
from util import settings

# Initialize AWS Controllers
global DYNAMODB
global LAMBDA
global IAM

DYNAMODB = boto3.client('dynamodb')
LAMBDA = boto3.client('lambda')
IAM_client = boto3.client('iam')
IAM_res = boto3.resource('iam')
    

# IAM Roles to Attach
global ROLES_ARN
ROLES_ARN = [
    'arn:aws:iam::aws:policy/AmazonSQSFullAccess', # SQS Full Access
    'arn:aws:iam::aws:policy/AWSLambdaFullAccess', # LAMBDA Full Access
    'arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess', # API Gateway Invocation Full Access
    'arn:aws:iam::aws:policy/CloudWatchFullAccess', # Cloudwatch Full Access
    'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess' # Dynamodb Full Access
]


# Create Dynamodb Table
def _create_table(tablename,indexName):
    global DYNAMODB

    DYNAMODB.create_table(
        AttributeDefinitions = [
            {
                'AttributeName' : indexName,
                'AttributeType' : 'S'
            }
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits' : 5,
            'WriteCapacityUnits' : 5
        },
        TableName = tablename,
        KeySchema = [
            {
                'AttributeName' : indexName,
                'KeyType' : 'HASH'
            }
        ]
    )


# AWS IAM Role Configuration
def _get_iam_role():
    global IAM_res
    global IAM_client
    global ROLES_ARN

    roleArn = ''
    # Try create serverless api
    try:
        response = IAM_client.create_role(
            RoleName = 'serverless-api',
            AssumeRolePolicyDocument = json.dumps({
                "Version" : "2012-10-17",
                "Statement" : [
                    {
                        "Effect" : "Allow",
                        "Principal" : {
                            "Service" : "lambda.amazonaws.com"
                        },
                        "Action" : ["sts:AssumeRole"]
                    }
                ]
            })
        )

        api_role = IAM_res.Role('serverless-api')
        roleArn = api_role.arn
        # attach policies
        for role in ROLES_ARN:
            print(role)
            api_role.attach_policy(
                PolicyArn = role
            )
            
        api_role.reload()

        print('==> Role created')
    except Exception as e:
        # Role resource Name already exist
        if('(EntityAlreadyExists)' in str(e)):
            api_role = IAM_res.Role('serverless-api')
            roleArn = api_role.arn
            print('==> Role created')
        else:
            print('Something went wrong.')
            print(str(e))

    return roleArn
    

# Create AWS Lambda Function
def _create_function(funcName):
    global LAMBDA

    # Generate IAM Role
    roleArn = _get_iam_role()

    # Compress This Directory
    file_name = 'zf.zip'
    cli_zip_cmd = 'zip -r '+file_name+' * -x .git/ .vscode/ @'
    os.system(cli_zip_cmd)
    zipFile = open('zf.zip','rb').read()

    response = LAMBDA.create_function(
        FunctionName = funcName,
        Runtime = 'python3.6',
        Role = roleArn,
        Handler = 'index.lambda_handler',
        Code = {
            "ZipFile" : zipFile
        },
        Timeout = 900
    )


# Add API service
def _create_service(service_name):
    template = open('services/template').read()
    fwriter = open('services/'+service_name+'.py','w')
    fwriter.write(template)
    fwriter.close()


# Execute Script
if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if(command == 'create_service'):
            print("Service Name: ")
            service_name = input()
            _create_service(service_name)
    else:
        print("Enter API Name: ")
        projname = input()
        settings._update('function_name',projname)
        try:
            _create_function(projname)
        except Exception as e:
            function_name = settings._value('function_name')
            file_name = 'zf.zip'
            cli_zip_cmd = 'zip -r '+file_name+' * -x .git/ .vscode/ @'
            cli_aws_cmd = 'aws lambda update-function-code --function-name '+function_name+' --zip-file fileb://zf.zip'
            os.system(cli_zip_cmd)
            os.system(cli_aws_cmd)           



