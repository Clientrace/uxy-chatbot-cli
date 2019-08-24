"""
Authored by Kim Clarence Penaflor
08/22/2019
Documented via reST

Application Logs Handler
"""

import os
import json
from uxy_cli._generators.aws_setup import AWSSetup

def getlogs():
  if( not os.path.isfile('uxy.json') ):
    print('Failed to locate app configuration file.')
    print('==> Deployment cancelled.')
    return

  try:
    config = json.loads(open('uxy.json').read())
  except Exception as e:
    print('App Configuration is not valid json format')
    raise Exception(e)

  awssetup = AWSSetup(config)
  print(awssetup.get_logs())

  

