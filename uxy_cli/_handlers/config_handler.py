"""
Authored By Kim Clarence Penaflor
09/01/2019
version 0.0.1

Configuration Handler
"""

import os
import json
import configparser
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
    return False

  if( not appconfigValidator.rule_validation_check() ):
    print('App configuration is invalid.')
    return False

  # Check deployment stage environment replacements
  if( deploymentStage not in config['app:config'] ):
    print('Deployment stage: '+deploymentStage\
      +' not in app configuration (uxy.json) app:config')
    return False

  return True

def _load_config_json(deploymentStage, projPath):
  """
  Load configuration json file (uxy.json)
  :param deploymentStage: application deployment stage
  :type deploymentStage: string
  """
  try:
    config = json.loads(open(projPath+'/uxy.json').read())
  except Exception as e:
    print('App Configuration is not valid json format.')
    raise Exception(e)

  deploymentStage = deploymentStage and deploymentStage or config['app:stage']
  if( not _validate_appconfig(config, deploymentStage)):
    raise Exception("App config invalid")

  return config, deploymentStage

def load_env_vars(projPath):
  """
  Load environment variables
  :param projPath: project path
  :type projPath: string
  """
  environment = configparser.ConfigParser()
  try:
    environment.read_file(open(projPath+'/src/env/environment.cfg'))
  except Exception as e:
    print('Failed to load environment configuration file')
    raise Exception(str(e))

  if( environment.get('FACEBOOK','FB_PAGE_TOKEN') == '' ):
    print('Facebook Page Token hasn\'t been set.')
    print('Configure the facebook page token in src/env/environment.cfg')
    raise Exception('Empty facebook page token')

  return environment

def get_config(projPath, deploymentStage):
  """
  Get APP Configuration Settings
  :param projPath: project path
  :type projPath: string
  :param deploymentStage: project deployment stage
  :type deploymentStage: string
  :returns: if configurations are complete
  :rtype: boolean
  """

  if( not os.path.isfile(projPath+'/uxy.json') ):
    raise Exception("Failed to locate app configuration file")

  config, deploymentStage = _load_config_json(deploymentStage, projPath)
  return config, deploymentStage


