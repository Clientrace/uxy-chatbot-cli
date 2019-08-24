"""
Authored By Kim Clarence Penaflor
08/08/2019
version 0.0.1

Project Setup Handler
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

  def create_dist(self):
    """
    Create APP Distributable
    """

    self.log('Creating Dist Package...')
    distPath = self.config['app:name']+'/.tmp/dist/'
    if( not os.path.exists(distPath) ):
      os.makedirs(distPath)

    for root, dirs, files in os.walk(self.config['app:name']):
      for file in files:
        fDir = os.path.join(root, file)
        if( '.git/' in fDir ):
          continue
        if( '.tmp/' in fDir ):
          continue
        fpath = fDir.replace(self.config['app:name']+'/','')
        froot = root.replace(self.config['app:name']+'/','')
        froot = root.replace(self.config['app:name'],'')

        if( not os.path.exists(distPath+froot) ):
          os.makedirs(distPath+froot)

        shutil.copyfile(fDir, distPath+fpath)

    for root, dirs, files in os.walk(self.config['app:name']+'/.tmp/dependencies'):
      for file in files:
        fDir = os.path.join(root, file)
        fpath = fDir.replace(self.config['app:name']+'/.tmp/dependencies/','')
        froot = root.replace(self.config['app:name']+'/.tmp/dependencies/','')

        if( not os.path.exists(distPath+froot) ):
          os.makedirs(distPath+froot)

        shutil.copyfile(fDir, distPath+fpath)

  def install_dependencies(self):
    """
    Install project dependencies
    """

    self.log('Installing dependencies...')
    distPath = self.config['app:name']+'/.tmp/dependencies'
    if( not os.path.exists(distPath) ):
      os.makedirs(distPath)
      os.system('pip3 install --system --prefix= requests -t '+distPath)

  def add_app_config(self):
    """
    Copy app config into newly created project
    """
    configFile = open(self.config['app:name']+'/uxy.json','w')
    configFile.write(json.dumps(self.config,indent=2,sort_keys=True))
    configFile.close()


  def clone(self):
    """
    Clone Project Repositry
    """
    self.log('Cloning project..')
    self.log('Cloning Uxy Chatbot Framework: '+self.chatbot_core_repo[self.config['app:runtime']])
    repo = git.Repo.clone_from(self.chatbot_core_repo[self.config['app:runtime']], self.config['app:name'])
    repo.remotes.origin.config_writer.set('pushurl','')
    repo.remotes.origin.config_writer.set('url','')

