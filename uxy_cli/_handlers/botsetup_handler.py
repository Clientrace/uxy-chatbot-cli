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
from uxy_cli._handlers import config_handler


def setup(deploymentStage):
  if( not os.path.isfile('uxy.json') ):
    print('Failed to locate app configuration file.')
    print('==> Deployment cancelled.')
    return

  config, deploymentStage = config_handler.get_config(os.getcwd(),\
    deploymentStage)

  environment = load_env_vars()
  fbBotSetup = FBBotSetup(environment, environment.get('FACEBOOK', 'FB_PAGE_TOKEN'), config)


