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
  :param config: application configuration
  :type config: dictionary
  :param cloudBlueprint: application aws resources blueprint
  :type cloudBlueprint: json
  :param environment: app environment configuration
  :type environment: configparser object
  """

  # compare checksums
  changeControl = ChangeControl(os.getcwd(), config)
  newChecksums, changeStatus = changeControl.compare_diff(cloudBlueprint['checksums'])
  return newChecksums, changeStatus


# TODO: Chatbot setup
def _chatbot_setup(config, environment, element, fbBotSetup):
  """
  Setup chatbot settings
  :param config: application configuration
  :type config: dictionary
  :param environment: app environment configuration
  :type environment: configparser object
  :param element: chatbot element to setup
  :type element: string (GET_STARTED, PERSISTENT_MENU, APP_DESCRIPTION, URL_WHITELIST)
  :param fbBotSetup: facebook chatbot setup
  :type fbBotSetup: FBBotSetup object
  """
  if( element == 'GET_STARTED' ):
    fbBotSetup.init_getstarted()
  if( element == 'APP_DESCRIPTION' ):
    fbBotSetup.init_bot_description()
  if( element == 'URL_WHITELIST' ):
    if( config['chatbot:config']['URLsToWhiteList'] != [] ):
      fbBotSetup.whitelist_urls()
  if( element == 'PERSISTENT_MENU' ):
    if( config['chatbot:config']['enable_menu'] ):
      fbBotSetup.init_persistent_menu()

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

    print('Replacing '+replacements['replace']+' with '+replacements['with']+'...')
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

  
  # Check for environment variables
  print('Setting environment variables...')
  _file_replacements(deploymentStage, config)

  environment = configparser.ConfigParser()
  # Load environment variables
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

  # Check FB_PAGE_TOKEN validity
  fbBotSetup = FBBotSetup(environment.get('FACEBOOK','FB_PAGE_TOKEN'), config)
  if( not fbBotSetup.check_token_validity() ):
    print('Please generate another token in app dashboard.')
    return

  awssetup = AWSSetup(config)
  cloudBlueprint = awssetup.load_cloud_config()

  print('Checking app updates...')
  newChecksums, update = _check_app_updates(config, cloudBlueprint, environment)
  if( update ):
    # Check setup update
    if( cloudBlueprint['deployment:count'] == 0 ):
      _chatbot_setup(config, environment, 'GET_STARTED', fbBotSetup)
      _chatbot_setup(config, environment, 'PERSISTENT_MENU', fbBotSetup)
      _chatbot_setup(config, environment, 'APP_DESCRIPTION', fbBotSetup)
      _chatbot_setup(config, environment, 'URL_WHITELIST', fbBotSetup)
    else:
      if( newChecksums['uxy.json'] != cloudBlueprint['checksums']['uxy.json'] ):
        if( config['chatbot:config']['persistent_menu'] != cloudBlueprint['chatbot:menu'] ):
          _chatbot_setup(config, environment, 'PERSISTENT_MENU', fbBotSetup)

        if( config['chatbot:config']['URLsToWhiteList'] != cloudBlueprint['chatbot:url_whitelist'] ):
          _chatbot_setup(config, environment, 'URL_WHITELIST', fbBotSetup)
        
        if( config['app:description'] != cloudBlueprint['app:description'] ):
          _chatbot_setup(config, environment, 'APP_DESCRIPTION', fbBotSetup)

  print('Updating applcation blueprint...')
  cloudBlueprint['checksums'] = newChecksums
  cloudBlueprint['deployment:count'] = cloudBlueprint['deployment:count'] + 1
  awssetup.save_cloud_config(cloudBlueprint)

  

  
  
