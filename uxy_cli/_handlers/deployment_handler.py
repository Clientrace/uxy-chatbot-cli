"""
Authored By Kim Clarence Penaflor
08/08/2019
version 0.0.1

Project Deployment handler
"""

import os
import json
import copy
import configparser
import hashlib
import shutil
from uxy_cli._handlers.change_control import ChangeControl
from uxy_cli._handlers.fb_bot_setup import FBBotSetup
from uxy_cli._validators.appconfig_validator import AppConfigValidator
from uxy_cli._generators.aws_setup import AWSSetup
from uxy_cli._handlers import setup_handler

def compile_spiels(path):
  """
  Compile Chatbot Spiels
  :param path: content path
  :type path: string
  :returns: combiled spiels json
  :rtype: dictionary
  """
  contentPath = path+'/src/content/spiels/'
  print(contentPath)

  spiels = {}
  for root, dirs, files in os.walk(contentPath):
    for file in files:
      fDir = os.path.join(root, file)
      spielFile = open(fDir).read()
      jsonContent = json.loads(spielFile)
      spiels = dict(spiels.items(), **jsonContent)

  return spiels

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

  changeControl = ChangeControl(os.getcwd(), config)
  cloudBlueprintCopy = copy.deepcopy(cloudBlueprint)
  cloudCheckSums = cloudBlueprintCopy['checksums']
  newChecksums, changeStatus = \
    changeControl.compare_diff(cloudCheckSums)

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
  :type element: string 
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
  print('Setting environment variables...')
  isFile = lambda path: os.path.isfile(path)
  for replacements in config['app:config'][stage]['fileReplacements']:
    if( not isFile(replacements['replace']) ):
      print('Failed to locate '+str(replacements['replace']))
      return False

    if( not isFile(replacements['with']) ):
      print('Failed to locate '+str(replacements['with']))
      return False

    print('Replacing '+replacements['replace']+' with '+replacements['with']\
      +'...')
    oldFile = open(replacements['replace'],'w')
    newFile = open(replacements['with']).read()
    oldFile.write(newFile)
    oldFile.close()

  return True

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


def load_env_vars():
  """
  Load environment variables
  """
  environment = configparser.ConfigParser()
  try:
    environment.read_file(open('src/env/environment.cfg'))
  except Exception as e:
    print('Failed to load environment configuration file')
    raise Exception(str(e))

  if( environment.get('FACEBOOK','FB_PAGE_TOKEN') == '' ):
    print('Facebook Page Token hasn\'t been set.')
    print('Configure the facebook page token in src/env/environment.cfg')
    raise Exception('Empty facebook page token')

  return environment


def setup_fb_bot(environment, awssetup, config):
  """
  Setup facebook chatbot
  """
  fbBotSetup = FBBotSetup(environment.get('FACEBOOK', 'FB_PAGE_TOKEN'), config)
  if( not fbBotSetup.check_token_validity() ):
    raise Exception('s3 bucket name not available.')

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
        if( config['chatbot:config']['persistent_menu']\
           != cloudBlueprint['chatbot:menu'] ):
          _chatbot_setup(config, environment, 'PERSISTENT_MENU', fbBotSetup)

        if( config['chatbot:config']['URLsToWhiteList']\
           != cloudBlueprint['chatbot:url_whitelist'] ):
          _chatbot_setup(config, environment, 'URL_WHITELIST', fbBotSetup)
        
        if( config['app:description'] != cloudBlueprint['app:description'] ):
          _chatbot_setup(config, environment, 'APP_DESCRIPTION', fbBotSetup)

  return cloudBlueprint, newChecksums


def create_dist():
  """
  Create APP Distributable
  """

  distPath = '.tmp/dist/'
  if( os.path.exists(distPath) ):
    shutil.rmtree(distPath)
    os.makedirs(distPath)

  
  spiels = compile_spiels(os.getcwd())
  os.makedirs(distPath+'src/content/spiels/')
  spielFile = open(distPath+'src/content/spiels/displays.json','w')
  spielFile.write(json.dumps(spiels,indent=4))
  spielFile.close()

  for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
      fDir = os.path.join(root, file)
      if( '.git/' in fDir ):
        continue
      if( '.tmp/' in fDir ):
        continue
      if( 'src/content/spiels/' in fDir):
        continue
      fpath = fDir.replace(os.getcwd()+'/','')
      froot = root.replace(os.getcwd()+'/','')
      froot = root.replace(os.getcwd(),'')

      if( not os.path.exists(distPath+froot) ):
        os.makedirs(distPath+froot)

      shutil.copyfile(fDir, distPath+fpath)

  for root, dirs, files in os.walk(os.getcwd()+'/.tmp/dependencies'):
    for file in files:
      fDir = os.path.join(root, file)
      fpath = fDir.replace(os.getcwd()+'/.tmp/dependencies','')
      froot = root.replace(os.getcwd()+'/.tmp/dependencies','')

      if( not os.path.exists(distPath+froot) ):
        os.makedirs(distPath+froot)

      shutil.copyfile(fDir, distPath+fpath)

def create_deployment_stage(stage, awssetup, config):
  """
  Creates new deployment stage
  """
  print("Creating new deployment stage..")
  setup_handler.setup_new_stage(config, stage)

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
  try:
    config, deploymentStage = load_config_json(deploymentStage)
    _file_replacements(deploymentStage, config)
    environment = load_env_vars()
    awssetup = AWSSetup(config)

    if( deploymentStage != 'dev' ):
      # Check if s3 bucket exists
      if( not awssetup.s3_bucket_exists(config['app:name']+'-uxy-app-'\
        +deploymentStage) ):
        create_deployment_stage(deploymentStage, awssetup, config)

    cloudBlueprint, newChecksums = setup_fb_bot(environment, awssetup, config)
    create_dist()
    awssetup.update_lambda()
  except Exception as e:
    print(str(e))
    print('==> Deployment cancelled')
    return


  print('Updating appilcation blueprint...')
  cloudBlueprint['checksums'] = newChecksums
  cloudBlueprint['deployment:count'] = cloudBlueprint['deployment:count'] + 1
  awssetup.save_cloud_config(cloudBlueprint)

  

