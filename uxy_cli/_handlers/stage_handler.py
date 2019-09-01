"""
Authored by Kim Clarence Penaflor
09/01/2019
version 0.0.1

Stage change handler
"""

import os
import json
import shutil
from uxy_cli._handlers import config_handler

def checkout(stage):
  """
  Checkout to a deployment stage
  :param stage: deployment stage
  :type stage: string
  """
  try:
    config, deploymentStage = config_handler.get_config(
      os.getcwd(),
      stage
    )
    print('Checking out to '+stage+' stage')
    shutil.copyfile('uxy.json', '.tmp/uxy.json')
    config['app:stage'] = stage
    configJsonFile = open('uxy.json','w')
    configJsonFile.write(json.dumps(config, indent=2))
    configJsonFile.close()
  except Exception as e:
    print('==> Checkout cancelled.')
    return

  print('==> Switched to '+stage+' stage')

 


