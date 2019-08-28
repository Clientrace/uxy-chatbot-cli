"""
Authored by Kim Clarence Penaflor
08/28/2019
version 0.0.1
Documented via reST

Uxy Component Generator
"""

import os
import json

class ComponentGenerator:
  """
  Generates spiel and unit component
  """

  verbosity = False

  def __init__(self, config):
    """
    Initialize application config
    """

    ComponentGenerator.verbosity = config['verbosity']
    self.config = config
    self.templateDir = os.getcwd()+'/uxy_cli/project_template'

  @classmethod
  def _log(cls, msg):
    """
    Log System Process
    :param msg: string msg to log
    :type msg: string
    """
    if( cls.verbosity ):
      print('[AWS]: ' + msg)

  def generate_spiel(self, acceptTypes):
    """
    Generate uxy chatbot spiel
    """

    tempDir = self.templateDir+'/spiel.json'
    template = json.loads(open(tempDir).read())
    template['acceptTypes'] = acceptTypes





