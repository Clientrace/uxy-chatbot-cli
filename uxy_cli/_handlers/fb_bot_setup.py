"""
Authorred By Kim Clarence Penaflor
08/18/2019
version 0.0.1

Facebook Chatbot Setup
"""

import requests

class FBBotSetup:


  HOST_URL = 'https://graph.facebook.com/v2.6'
  verbosity = False
  
  def __init__(self, pageToken, config):
    """
    Initialize facebook page token and menu blueprint
    :param pageToken: facebook app page token
    :type pageToken: string
    :param config: application configuration
    :type config: string
    """

    FBBotSetup.verbosity = config['verbosity']
    self.accessToken = pageToken
    self.config = config


  @classmethod
  def _log(cls, msg):
    """
    Log System Process
    :param msg: string msg to log
    :type msg: string
    """
    if( cls.verbosity ):
      print('[FB_SETUP]: '+msg)

  def init_persistent_menu(self):
    """
    Initialize Facebook chatbot's persistent menu
    """
    FBBotSetup._log("+ Initializing Bot Peristent Menu...")
    URL = self.HOST_URL + '/me/messenger_profile?access_token='+self.accessToken
    persistConfig = self.config['chatbot:config']['persistent_menu']
    resp = requests.post(
      URL,
      json = persistConfig
    )
    if( resp.status_code != 200 ):
      FBBotSetup._log("Setup Failed.")
    else:
      FBBotSetup._log("=> Success.")

  


