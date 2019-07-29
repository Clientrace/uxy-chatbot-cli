import os

def var(key):
  return os.environ[key]

def environment():
  return os.environ['stage']


