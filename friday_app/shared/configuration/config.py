import os
import json

global DEFAULTS
DEFAULTS = json.loads(open('friday_app/shared/configuration/default_config.json').read())

def var(key):
  global DEFAULTS
  if(key in os.environ):
    return os.environ[key]
  return DEFAULTS[key]

def environment():
  global DEFAULTS
  if('stage' in os.environ):
    return os.environ['stage']
  return DEFAULTS['stage']




