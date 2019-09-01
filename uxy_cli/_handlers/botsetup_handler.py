"""
Authored by Kim Clarence Penaflor
01/01//2019
version 0.0.1
Documented via reST

Setup Bot Config
"""

import os
import configparser
from uxy_cli._handlers.fb_bot_setup import FBBotSetup


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


def setup(deploymentStage):
  if( not os.path.isfile('uxy.json') ):
    print('Failed to locate app configuration file.')
    print('==> Deployment cancelled.')
    return

  environment = load_env_vars()
  fbBotSetup = FBBotSetup(environment, environment.get('FACEBOOK', 'FB_PAGE_TOKEN'), config)
