"""
Authored By Kim Clarence Penaflor
08/08/2019
version 0.0.1

Project Deployment handler
"""

import os
import json
import configparser

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

def deploy(config, deploymentStage):
  """
  Deploy chatbot project
  """
  deploymentStage = deploymentStage and deploymentStage or config['app:stage']

  # Check deployment stage environment replacements
  if( deploymentStage not in config['app:config'] ):
    print('Deployment stage: '+deploymentStage+' not in app configuration (uxy.json) app:config')
    return

  # Look for app configuration file
  if( not os.path.isfile('uxy.json') ):
    print('Failed to locate app configuration file.')
    return

  environment = configparser.ConfigParser()
  environment = environment.read('src/env/environment.cfg')




  



