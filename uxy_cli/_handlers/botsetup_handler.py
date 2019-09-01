"""
Authored by Kim Clarence Penaflor
08/31//2019
version 0.0.1
Documented via reST

Setup Bot Config
"""

import os
import configparser
from uxy_cli._handlers.fb_bot_setup import FBBotSetup
from uxy_cli._handlers import config_handler


def setup_bot(config, environment, element, fbBotSetup):
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
  if( element == 'start' ):
    fbBotSetup.init_getstarted()
  if( element == 'desc' ):
    fbBotSetup.init_bot_description()
  if( element == 'whitelist' ):
    if( config['chatbot:config']['URLsToWhiteList'] != [] ):
      fbBotSetup.whitelist_urls()
  if( element == 'menu' ):
    if( config['chatbot:config']['enable_menu'] ):
      fbBotSetup.init_persistent_menu()

def setup(component, deploymentStage):
  """
  Apply chatbot setup
  :param component: component to update
  :type component: string
  """

  if( not os.path.isfile('uxy.json') ):
    print('Failed to locate app configuration file.')
    print('==> Deployment cancelled.')
    return

  try:
    config, deploymentStage = config_handler.get_config(os.getcwd(),\
      deploymentStage)

    environment = config_handler.load_env_vars(os.getcwd())
    fbBotSetup = FBBotSetup(environment.get('FACEBOOK','FB_PAGE_TOKEN'),\
      config)

    setup_bot(config, environment, component, fbBotSetup)

  except Exception as e:
    print("==> Setup cancelled.")
    return



