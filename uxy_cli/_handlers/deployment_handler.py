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
from uxy_cli._handlers.change_control import ChangeControl
from uxy_cli._handlers.fb_bot_setup import FBBotSetup
from uxy_cli._validators.appconfig_validator import AppConfigValidator
from uxy_cli._generators.aws_setup import AWSSetup


def _check_app_updates(config, cloudBlueprint, environment):
  """
  Check application updates for deployment
  """

  # compare checksums
  changeControl = ChangeControl('.', config)
  changeControl.compare_diff(cloudBlueprint['checksums'])


# TODO: Chatbot setup
def _chatbot_setup(config, environment, element):
  """
  Setup chatbot settings
  :param config: application configuration
  :type config: dictionary
  :param environment: app environment configuration
  :type environment: configparser object
  :param element: chatbot element to setup
  :type element: string (PERSISTENT_MENU, APP_DESCRIPTION, URL_WHITELIST)
  """
  fbBotSetup = FBBotSetup(environment.get('FACEBOOK','FB_PAGE_TOKEN'), config)
  if( element == 'PERSISTENT_MENU' ):
    if( config['chatbot:config']['enable_menu'] ):
      fbBotSetup.init_persistent_menu()
  if( element == 'APP_DESCRIPTION' ):
    fbBotSetup.init_bot_description()
  if( element == 'URL_WHITELIST' ):
    fbBotSetup.whitelist_urls()

def _file_replacements(stage, config):
  """
  File Replacement In Deployment Environment
  :param stage: deployment stage
  :type stage: string
  :param config: application configuration
  :type config: dictionary
  :returns: replacement successful
  :rtype: boolean
  """
  isFile = lambda path: os.path.isfile(path)
  for replacements in config['app:config'][stage]['fileReplacements']:
    if( not isFile(replacements['replace']) ):
      print('Failed to locate '+str(replacements['replace']))
      return False

    if( not isFile(replacements['with']) ):
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


def _validate_appconfig(config, deploymentStage):
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
    print('Deployment stage: '+deploymentStage+' not in app configuration (uxy.json) app:config')
    print('==> Deployment cancelled.')
    return False

  return True

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

  deploymentStage = deploymentStage and deploymentStage or config['app:stage']
  if( not _validate_appconfig(config, deploymentStage) ):
    return

  environment = configparser.ConfigParser()
  # Load environemnt variables
  try:
    environment.read_file(open('src/env/environment.cfg'))
  except Exception as e:
    print(e)
    print('Failed to load environment configuration file')
    return

  if( environment.get('FACEBOOK','FB_PAGE_TOKEN') == '' ):
    print('Facebook Page Token hasn\'t been set.')
    print('Configure the facebook page token in src/env/environment.cfg')
    return

  # Check for environment variables
  print('Setting environment variables...')
  _file_replacements(deploymentStage, config)

  awssetup = AWSSetup(config)
  cloudBlueprint = awssetup.load_cloud_config()
  print(cloudBlueprint)


  
  


