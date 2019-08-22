"""
Authored by Kim Clarence Penaflor
08/23//2019
version 0.0.1
Documented via reST

Get Project uxy Info
"""

import json
from uxy_cli._generators.aws_setup import AWSSetup
from uxy_cli._validators.appconfig_validator import AppConfigValidator

def _validate_appconfig(config, deploymentStage):
  """
  Validate app configuration file
  :param config: application configuration
  :type config: dictionary
  :param deploymentStage: application deployment stage
  :type deploymentStage: string
  :returns: app config validility
  :rtype: boolean
  """
  appconfigValidator = AppConfigValidator(config)
  if( not appconfigValidator.attrib_check() ):
    print('App configuration is invalid. Missing some key parameters')
    print('==> Deployment cancelled.')
    return False

  if( not appconfigValidator.rule_validation_check() ):
    print('App configuration is invalid.')
    print('==> Deployment cancelled.')
    return False

  # Check deployment stage environment replacements
  if( deploymentStage not in config['app:config'] ):
    print('Deployment stage: '+deploymentStage\
      +' not in app configuration (uxy.json) app:config')
    print('==> Deployment cancelled.')
    return False

  return True

def load_config_json(deploymentStage):
  """
  Load configuration json file (uxy.json)
  :param deploymentStage: application deployment stage
  :type deploymentStage: string
  """
  try:
    config = json.loads(open('uxy.json').read())
  except Exception as e:
    print('App Configuration is not valid json format.')
    raise Exception(e)

  deploymentStage = deploymentStage and deploymentStage or config['app:stage']
  if( not _validate_appconfig(config, deploymentStage)):
    raise Exception(e)

  return config, deploymentStage

def get_cloud_blueprint(deploymentStage):
  """
  Get aws resources blueprint
  """

  config, deploymentStage = load_config_json(deploymentStage)
  config['app:stage'] = deploymentStage
  awssetup = AWSSetup(config)
  cloudBlueprint = awssetup.load_cloud_config()
  print('Deployment Count: '+str(cloudBlueprint['deployment:count']))
  print('IAM ARN: '+cloudBlueprint['iam:arn'])
  print('Lambda ARN: '+cloudBlueprint['lambda:arn'])
  print('Invocation URL: '+cloudBlueprint['restApi:invokeURL'])



