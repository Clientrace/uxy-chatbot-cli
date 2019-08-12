"""
"""

import os
import git
import json
import shutil
import uxy_cli

class ProjSetup:
  """
  """

  # Uxy Chatbot Core Reporsitory http url
  chatbot_core_repo = {
    'python' : 'https://github.com/Clientrace/uxy-framework-python.git'
  }

  def __init__(self, config):
    self.config = config


  def log(self, msg):
    if( self.config['verbosity'] ):
      print('[SETUP] : '+msg)


  def _add_app_config(self):
    """
    Copy app config into newly created project
    """
    configFile = open(self.config['app:name']+'/uxy.json','w')
    configFile.write(json.dumps(self.config,indent=2,sort_keys=True))
    configFile.close()


  def _clone(self):
    """
    Clone Project Repositry
    """
    self.log('Cloning project..')
    self.log('Cloning Uxy Chatbot Framework: '+self.chatbot_core_repo)
    repo = git.Repo.clone_from(self.chatbot_core_repo[self.config['app:runtime']], self.config['app:name'])
    repo.remotes.origin.config_writer.set('pushurl','')
    repo.remotes.origin.config_writer.set('url','')




