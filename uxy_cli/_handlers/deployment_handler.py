"""
Authored By Kim Clarence Penaflor
08/08/2019
version 0.0.1

Project Deployment handler
"""

import os
import json
import configparser
import hashlib
from uxy_cli._validators.appconfig_validator import AppConfigValidator

def _file_replacements(stage, config):
  """
  File Replace In Deployment Environment
  :param stage: deployment stage
  :type stage: string
  :param config: application configuration
  :type config: dictionary
  :returns: replacement successful
  :rtype: boolean
  """
  isFile = lambda path: os.path.isfile(path)
  for replacements in config['app:config'][stage]:
    if( isFile(replacements['replace']) ):
      print('Failed to locate '+str(replacements['replace']))
      return False

    if( isFile(replacements['with']) ):
      print('Failed to locate '+str(replacements['with']))
      return False

    oldFile = open(replacements['replace'],'w')
    newFile = open(replacements['with']).read()
    oldFile.write(newFile)
    oldFile.close()

  return True


def load_config_json():
  """
  Load configuration json file (uxy.json)
  """
  try:
    config = json.loads(open('uxy.json').read())
    return config
  except Exception as e:
    print('App Configuration is not valid json format.')
  return None

def deploy(deploymentStage):
  """
  Deploy chatbot project
  :param deploymentStage: application deployment stage
  :type deploymentStage: string
  """

  # Look for app configuration file
  if( not os.path.isfile('uxy.json') ):
    print('Failed to locate app configuration file.')
    print('==> Deployment cancelled.')
    return

  # Validate App Config
  config = load_config_json()
  if( not config ):
    print('==> Deployment cancelled.')
    return

  appconfigValidator = AppConfigValidator(config)
  if( appconfigValidator.attrib_check() ):
    print('App configuration is invalid. Missing some key parameters')
    print('==> Deployment cancelled.')

  if( appconfigValidator.rule_validation_check() ):
    print('App configuration is invalid.')
    print('==> Deployment cancelled.')

  # Check deployment stage environment replacements
  if( deploymentStage not in config['app:config'] ):
    print('Deployment stage: '+deploymentStage+' not in app configuration (uxy.json) app:config')
    print('==> Deployment cancelled.')
    return

  print('Setting environment variables...')
  deploymentStage = deploymentStage and deploymentStage or config['app:stage']
  _file_replacements(deploymentStage, config)

  environment = configparser.ConfigParser()
  environment = environment.read('src/env/environment.cfg')






  