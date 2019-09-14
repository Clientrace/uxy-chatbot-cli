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
from uxy_cli._generators.aws_setup import AWSSetup
from uxy_cli._handlers import setup_handler
from uxy_cli._handlers import config_handler

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

def setup_fb_bot(environment, awssetup, config):
  """
  Setup facebook chatbot
  """
  fbBotSetup = FBBotSetup(environment.get('FACEBOOK', 'FB_PAGE_TOKEN'), config)
  if( not fbBotSetup.check_token_validity() ):
    raise Exception('FB Token not valid.')

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


def assess_deployment_stage(awssetup, config, stage):
  """
  Assess deployment stage if everything is already setup up before
  :param awssetup: Aws Setup Manager
  :type awssetup: AWSSetup Object
  :param config: app configuraoitn
  :type config: dictionary
  :param stage: app deployment stage
  :type stage: string
  """

  bucketName = config['app:name'] + '-uxy-app-' + stage
  if( not awssetup.s3_bucket_exists(bucketName) ):
    create_deployment_stage(stage, awssetup, config)
    return True
  elif( not awssetup.s3_object_exists(bucketName, 'aws_blueprint.json') ):
    print('Creating deployment stage')
    create_deployment_stage(stage, awssetup, config)
    return True

  return False

def rewrite_stage(config, stage):
  """
  Rewrite Stage
  :param config: app configuration
  :type config: string
  :param stage: app deployment stage
  :type stage: string
  """
  shutil.copyfile('uxy.json', '.tmp/uxy.json')
  config['app:stage'] = stage
  configJsonFile = open('uxy.json','w')
  configJsonFile.write(json.dumps(config, indent=2))
  configJsonFile.close()
  

def deploy(deploymentStage):
  """
  Deploy chatbot project
  :param deploymentStage: application deployment stage
  :type deploymentStage: string
  """

  # Validate App Config
  try:
    config, deploymentStage = config_handler.get_config(os.getcwd(),\
       deploymentStage)

    print("Deploying on "+deploymentStage)
    _file_replacements(deploymentStage, config)
    environment = config_handler.load_env_vars(os.getcwd())
    awssetup = AWSSetup(config)

    rewrite_stage(config, deploymentStage)
    if( deploymentStage != 'dev' ):
      # Check if s3 bucket exists
      assess_deployment_stage(awssetup, config, deploymentStage)

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

  

