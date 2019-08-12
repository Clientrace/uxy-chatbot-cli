"""
Authored by Kim Clarence Penaflor
08/12//2019
version 0.0.2
Documented via reST

Project uxy cli clueanup handler module
"""

import json
import os
import shutil
from uxy_cli._generators.aws_setup import AWSSetup


def __remove_dynamodb(awssetup, cloudBlueprint):
  print('Removing Dynamodb Table...')
  try:
    awssetup.remove_dynamodb_table(cloudBlueprint['dynamodb:name'])
    AWSSetup._log('=> Table deleted..')
  except Exception as e:
    if( '(ResourceNotFoundException)' in str(e) ):
      AWSSetup._log('=> Table already deleted')

def __remove_iamRole(awssetup, cloudBlueprint):
  print('Removing Iam Role...')
  try:
    awssetup.remove_iamrole(cloudBlueprint['iam:name'])
    AWSSetup._log('=> IAM Role deleted')
  except Exception as e:
    if( '(ResourceNotFoundException)' in str(e) ):
      AWSSetup._log('=> IAM Role already deleted')

def __remove_apiGateway(awssetup, cloudBlueprint):
  print('Removing Rest API...')
  try:
    awssetup.delete_apigateway_rest(cloudBlueprint['restApi:id'])
    AWSSetup._log('=> Rest API Deleted.')
  except Exception as e:
    if( '(ResourceNotFoundException)' in str(e) ):
      AWSSetup._log('=> Rest API already Deleted.')

def __remove_lambda_function(awssetup, cloudBlueprint):
  print('Removing Lambda Function...')
  try:
    awssetup.remove_lambda(cloudBlueprint['lambda:name'])
    AWSSetup._log('=> Lambda function deleted.')
  except Exception as e:
    if( '(ResourceNotFoundException)' in str(e) ):
      AWSSetup._log('=> Lambda function already Deleted.')

def purge():
  if( not os.path.isfile('uxy.json') ):
    print('Failed to locate app configuration file..')
  else:
    appConfig = json.loads(open('uxy.json').read())
    awssetup = AWSSetup(appConfig)

    print('Loading application cloud blueprint...')
    try:
      cloudBlueprint = awssetup.load_cloud_config()
      __remove_iamRole(awssetup, cloudBlueprint)
      __remove_dynamodb(awssetup, cloudBlueprint)
      __remove_apiGateway(awssetup, cloudBlueprint)
      __remove_lambda_function(awssetup, cloudBlueprint)
    except Exception as e:
      print('Failed to load cloud blueprint.')
      print('Try manually removing AWS resources.')

    print('Removing project files...')
    os.remove('.')
    print('=> Project removed.')


