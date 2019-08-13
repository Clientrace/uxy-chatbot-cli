"""
Authored By Kim Clarence Penaflor
08/08/2019
version 0.0.1

Project Deployment handler
"""

import os
import configparser


class DeploymentHandler():

  def __init__(self, config):
    self.config = config
    self.environment = configparser.ConfigParser()


  def deploy(self):
    """
    Deploy chatbot project
    """

    # Checks for FB PAGE TOKEN
    if( configparser.ConfigParser() ):
      self.environment.read('src/env/environment.cfg')

    # Look for app configuration file
    if( not os.path.isfile('uxy.json') ):
      print('Failed to locate app configuration file.')
      pass


