"""
Authored by Kim Clarence Penaflor
08/09//2019
version 0.0.3
Documented via reST

Project uxy cli setup command manager module
"""

import uuid
import time
import os
import json
import uxy_cli
from uxy_cli._generators.aws_setup import AWSSetup
from uxy_cli._generators.proj_setup import ProjSetup
from uxy_cli._handlers.change_control import ChangeControl


def _project_setup(config):
  """
  Initial Project Setup
  :param config: app configuration
  :type config: dictionary
  """

  fbVerifyToken = uuid.uuid4().hex
  config['fb:verifyToken'] = fbVerifyToken

  print('Loading project...')
  projsetup = ProjSetup(config)
  projsetup.clone()
  projsetup.add_app_config()
  projsetup.install_dependencies()
  projsetup.create_dist()


def _create_lambda(awssetup, iamRoleARN, projPath):
  """
  Wait for iam role until it is generated
  :param awssetup: Amazon Setup Module
  :type awssetp: AwsSetup Object
  :param iamRoleARN: iam role aws resouce name
  :type iamRoleARN: string
  :param projPath: project path
  :type projPath: string
  """
  while True:
    try:
      lambdaARN = awssetup.package_lambda(iamRoleARN, projPath)
      break
    except Exception as e:
      print(str(e))
      print('IAM Resource not yet available, Retrying Lambda Creation...')
      pass
    time.sleep(5)
  return lambdaARN

def _create_s3_bucket(awssetup):
  """
  Wait for s3 bucket setup
  :param awssetup: Amazon Setup Module
  :type awssetp: AwsSetup Object
  """
  status = awssetup.setup_s3_bucket()
  if not status :
    print('Please use other application name..')
  return status

def _aws_setup(config, region, projPath):
  """
  AWS Resource setup
  """

  print('Creating AWS Resources...')
  awssetup = AWSSetup(config)
  awssetup.setup_dynamodb_table()

  s3Status = _create_s3_bucket(awssetup)
  if( not s3Status ):
    return None

  appName, stage = config['app:name'], config['app:stage']
  dynamodbName = appName + '-uxy-session-' + stage
  iamRoleARN = awssetup.setup_iamrole()
  lambdaARN = _create_lambda(awssetup, iamRoleARN, projPath)
  restApi = awssetup.setup_uxy_api(lambdaARN)
  changeControl = ChangeControl(appName, config)
  checksums = changeControl.generate_filechecksums()
  
  projectBlueprint = {
    'app:name' : appName,
    'app:region' : region,
    'app:description' : config['app:description'],
    'iam:roles' : config['aws:config']['iam:roles'],
    'chatbot:menu' : config['chatbot:config']['persistent_menu'],
    'chatbot:url_whitelist' : config['chatbot:config']['URLsToWhiteList'],
    'deployment:count' : 0,
    'dynamodb:name' : dynamodbName,
    'iam:arn' : iamRoleARN,
    'iam:name' : appName + 'uxy-app',
    'lambda:arn' : lambdaARN,
    'lambda:name' : appName + '-uxy-app-' + stage,
    'restApi:id' : restApi['restApiId'],
    'restApi:invokeURL' : restApi['invokeURL'],
    's3:name' : appName + '-uxy-app-' + stage,
    'checksums' : checksums
  }

  awssetup.save_cloud_config(projectBlueprint)
  return restApi

def setup_new_stage(config, stage):
  """
  Setup New AWS Stage
  :param config: 
  """

  # Edit current deployment stage
  config['app:stage'] = stage
  apigateway = _aws_setup(config, stage, os.getcwd())

  if( not apigateway ):
    print('Project Setup Aborted..')
    return

def setup(appname, runtime, description, stage, region):
  """
  Setup AWS Resources needed
  :param appname: application name
  :type appname: string
  :param runtime: application runtime
  :type runtime: string
  :param description: application short description
  :type description: string
  :param stage: app stage, this also serves as the deployment env.
  :type stage: string
  :param region: aws region
  :type region: string
  """

  appconfig = json.loads(open(uxy_cli.ROOT_DIR+'/project_template/uxy.json').read())
  appconfig['app:name'] = appname
  appconfig['app:version'] = '1'
  appconfig['app:description'] = description
  appconfig['app:runtime'] = runtime
  appconfig['app:stage'] = stage
  appconfig['aws:config']['region'] = region
  
  _project_setup(appconfig)
  apigateway = _aws_setup(appconfig, region, appname)

  if( not apigateway ):
    print('Project Setup Aborted..')
    return

  print('==> Project successfully created!')
  print('API Invocation URL: '+apigateway['invokeURL'])
  print('Use this url to integrate with a facebook app.')
  print('Deploy project with: uxy deploy --[stage]')
  
    


 