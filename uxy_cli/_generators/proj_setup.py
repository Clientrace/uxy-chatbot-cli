"""
"""

import os
import git

class ProjSetup:
  """
  """

  # Uxy Chatbot Core Reporsitory http url
  chatbot_core_repo = 'https://github.com/Clientrace/uxy-chatbot-framework.git'

  def __init__(self, config):
    self.config = config

  def _clone(self):
    """
    Clone Project Repositry
    """

    os.mkdir(self.config['app:name'])
    repo = git.Repo.clone_from(self.chatbot_core_repo, self.config['app:name'])
    repo.remotes.origin.config_writer.set('pushurl','')
    repo.remotes.origin.config_writer.set('fetchurl','')




