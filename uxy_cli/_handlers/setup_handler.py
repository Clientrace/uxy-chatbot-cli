"""
Authored by Kim Clarence Penaflor
08/09//2019
version 0.0.2
Documented via reST

Project uxy cli setup command manager module
"""

import time
import os
import json
import uxy_cli
from uxy_cli._generators.aws_setup import AWSSetup
from uxy_cli._generators.proj_setup import ProjSetup
from uxy_cli._handlers.change_control import ChangeControl

global ROOT_DIR
global _appconfig
global _awssetup
global _projsetup
global _projectBlueprint

_projectBlueprint = {}


def _project_setup():
  """
  Initial Project Setup
  """

  global _appconfig

  print('Loading project...')
  projsetup = ProjSetup(_appconfig)
  projsetup._clone()
  projsetup._add_app_config()


def _save_project_blueprint(key, value):
  global _projectBlueprint
  """
  Saves project blueprint for backup
  :param key: json key
  :type key: string
  :param value: json value
  :type value: string
  """

  _projectBlueprint[key] = value

def _create_lambda(awssetup, iamRoleARN):
  """
  Wait for iam role until it is generated
  :param awssetup: Amazon Setup Module
  :type awssetp: AwsSetup Object
  :param iamRoleARN: iam role aws resouce name
  :type iamRoleARN: string
  """
  while True:
    try:
      lambdaARN = awssetup.package_lambda(iamRoleARN)
      break
    except Exception as e:
      pass
    time.sleep(5)
  return lambdaARN


def _aws_setup():
  """
  AWS Resource setup
  """
  global _appconfig
  global _projectBlueprint

  print('Creating AWS Resources...')
  awssetup = AWSSetup(_appconfig)
  awssetup.setup_dynamodb_table()
  _save_project_blueprint('dynamodb:name', _appconfig['app:name']+'-uxy-session-'+_appconfig['app:stage'])

  iamRoleARN = awssetup.setup_iamrole()
  _save_project_blueprint('iam:arn', iamRoleARN)
  _save_project_blueprint('iam:name', _appconfig['app:name']+'-uxy-app')

  lambdaARN = _create_lambda(awssetup, iamRoleARN)

  _save_project_blueprint('lambda:arn', lambdaARN)
  _save_project_blueprint('lambda:name', _appconfig['app:name']+'-uxy-app-'+_appconfig['app:stage'])

  restApi = awssetup.setup_uxy_api(lambdaARN)
  _save_project_blueprint('restApi:id', restApi['restApiId'])

  _save_project_blueprint('s3:name', _appconfig['app:name']+'-uxy-app-'+_appconfig['app:stage'])

  print('Saving file checksums...')
  changeControl = ChangeControl(_appconfig['app:name'], _appconfig)
  checksums = changeControl.generate_filechecksums()
  _save_project_blueprint('checksums', checksums)
  awssetup.save_cloud_config(_projectBlueprint)

  return restApi


def _setup_(appname, runtime, description, stage, region):
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
  :type regtion: string
  """

  global _appconfig
  _appconfig = json.loads(open(uxy_cli.ROOT_DIR+'/project_template/uxy.json').read())

  print('\nCreating project: '+appname+'...')

  _appconfig['app:name'] = appname
  _appconfig['app:version'] = '1'
  _appconfig['app:description'] = description
  _appconfig['app:runtime'] = runtime
  _appconfig['app:stage'] = stage
  _appconfig['aws:config']['region'] = region

  _save_project_blueprint('app:name', appname)
  _save_project_blueprint('app:region', region)
  _save_project_blueprint('iam:roles', _appconfig['aws:config']['iam:roles'])

  _project_setup()
  apigateway = _aws_setup()

  print('==> Project successfully created!')
  print('API Invocation URL: '+apigateway['invokeURL'])
  print('Use this url to integrate with a facebook app.')
  print('Deploy project with: uxy deploy --[stage]')





