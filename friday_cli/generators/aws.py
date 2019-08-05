"""
Authored by Kim Clarence Penaflor
08/05/2019
version 0.0.01
Documented via reST

AWS Development Environment Setup
"""

import boto3
import uuid
import json
from friday_app.shared.configuration import config

global _s3
global _dynamodb
global _IAMRolesARN

global _IAMRes
global _IAMClient

# IAM Roles to attach
_iamRolesARN = [
  'arn:aws:iam::aws:policy/AmazonSQSFullAccess', # SQS Full Access
  'arn:aws:iam::aws:policy/AWSLambdaFullAccess', # LAMBDA Full Access
  'arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess', # API Gateway Invocation Full Access
  'arn:aws:iam::aws:policy/CloudWatchFullAccess', # Cloudwatch Full Access
  'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess' # Dynamodb Full Access
]

_dynamodb = boto3.resource('dynamodb')
_s3 = boto3.client('s3')
_IAMRes = boto3.resource('iam')
_IAMClient = boto3.client('iam')


# TODO: Save Cloud Config
def _save_cloud_config():
  pass


# Initialize Dynamodb Table
# TODO: Initialize Dynamodb Table
def _init_table():
  global _dynamodb
  pass


# TODO: Initialize IAM Role
def __generate_iam_role(appName):
  global _IAMRolesARN
  global _IAMRes
  global _IAMClient

  print('')
  roleName = appName+'-friday-app-role'
  try:
    _IAMClient.create_role(
      RoleName = roleName,
      AssumeRolePolicyDocument = json.dumps({
        'Version' : '2012-10-17',
        'Statement' : [{
          'Effect' : 'Allow',
          'Principal' : {
            'Service' : 'lambda.amazonaws.com'
          },
          'Action' : ['sts:AssumeRole']
        }]
      })
    )
    apiRole = IAM_res.Role(roleName)
    for role in _IAMRolesARN:
      print('[Attaching]: ')
  except Exception as e:
    if( 'EntityAlreadyExists' in str(e) ):
      apiRole = _IAMRes.Role(appName+'-friday-app-role')
      roleARN = apiRole.arn









