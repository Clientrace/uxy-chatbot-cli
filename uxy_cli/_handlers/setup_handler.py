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

logging.basicConfig(level=logging.INFO)

_appconfig = json.loads(open('project_template/uxy.json').read())

# TODO: Setup AWS Resources
def __setup_aws_resources():
  global _appconfig

  # Project Setup
  _projsetup = ProjSetup(_appconfig)
  _projsetup.

  # AWS Resource setup
  _awssetup = AWSSetup(_appconfig)
  logging.info('AWS Setup...')
  roleARN = _awssetup.setup_iamrole()
  _awssetup.package_lambda(roleARN)
  _awssetup.setup_uxy_api()


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

  logging.info('APPNAME: '+appname)
  logging.info('RUNTIME: '+runtime)
  logging.info('DESCRIPTION: '+description)
  logging.info('REGION: '+description)
  logging.info('Loading application config template...')

  _appconfig['app:name'] = appname
  _appconfig['app:description'] = description
  _appconfig['app:runtime'] = runtime
  _appconfig['app:stage'] = stage
  _appconfig['aws:config']['region'] = region









