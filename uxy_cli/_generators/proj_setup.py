"""
"""

import os
import git
import json

class ProjSetup:
  """
  """

  # Uxy Chatbot Core Reporsitory http url
  chatbot_core_repo = 'https://github.com/Clientrace/uxy-chatbot-framework.git'

  def __init__(self, config):
    self.config = config


  def _add_app_config(self):
    """
    Copy app config into newly created project
    """
    configFile = open('uxy.json','w')
    configFile.write(json.dumps(self.config,indent=2,sort_keys=True))
    configFile.close()

  def _clone(self):
    """
    Clone Project Repositry
    """

    os.mkdir(self.config['app:name'])
    repo = git.Repo.clone_from(self.chatbot_core_repo, self.config['app:name'])
    repo.remotes.origin.config_writer.set('pushurl','')
    repo.remotes.origin.config_writer.set('url','')




