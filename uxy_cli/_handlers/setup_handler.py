"""
Authored by Kim Clarence Penaflor
08/09//2019
version 0.0.2
Documented via reST

Project uxy cli command manager module
"""

import json
import logging
from uxy_cli._generators.aws_setup import AWSSetup
from uxy_cli._generators.proj_setup import ProjSetup

global _appconfig
global _awssetup
global _projsetup

_appconfig = json.loads(open('uxy_cli/project_template/uxy.json').read())

def _project_setup():
  """
  Initial Project Setup
  """

  global _appconfig
  print('Loading project...')
  projsetup = ProjSetup(_appconfig)
  projsetup._clone()
  projsetup._add_app_config()

def _aws_setup():
  """
  AWS Resource setup
  """

  global _appconfig

  print('Creating AWS Resources...')
  awssetup = AWSSetup(_appconfig)
  iamRoleARN = awssetup.setup_iamrole()
  lambdaARN = awssetup.package_lambda(iamRoleARN)
  awssetup.setup_uxy_api(lambdaARN)


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

  print('\nCreating project: '+appname+'...')

  _appconfig['app:name'] = appname
  _appconfig['app:description'] = description
  _appconfig['app:runtime'] = runtime
  _appconfig['app:stage'] = stage
  _appconfig['aws:config']['region'] = region

  _project_setup()
  _aws_setup()


