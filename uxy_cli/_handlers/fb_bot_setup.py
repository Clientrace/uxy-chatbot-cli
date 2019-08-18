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


  def check_token_validity(self):
    """
    Checks wether the page access token is valid
    :returns: indicate if token is valid
    :rtype: boolean
    """
    FBBotSetup._log("Checking Page Token validity...")
    URL = self.HOST_URL+'/me?access_token='+self.accessToken
    resp = requests.get(URL)
    if( resp.status_code == 200 ):
      return True

    FBBotSetup._log('Invalid Page Token.')
    return False


  def init_bot_description(self):
    """
    Initialize Chatbot Initial Greeting/ Description
    """
    FBBotSetup._log("+ Initializing Bot Description...")
    URL = self.HOST_URL + '/me/messenger_profile?access_token='+self.accessToken
    payload = {
      'greeting' : [{
          'locale' : 'default',
          'text' : self.config['app:description']
      }]
    }
    resp = requests.post(
      URL,
      json = payload
    )
    if( resp.status_code != 200 ):
      FBBotSetup._log('Setup Failed.')
    else:
      FBBotSetup._log('=> Success.')


  def whitelist_urls(self):
    """
    Whitelist chatbot webview urls
    """
    FBBotSetup._log("+ Whitelisting URLs...")
    URL = self.HOST_URL + '/me/messenger_profile?access_token='+self.accessToken
    payload = {
      'setting_type' : 'domain_whitelisting',
      'whitelisted_domains' : self.config['chatbot:config']['URLsToWhiteList'],
      'domain_action_type' : 'add'
    }
    resp = requests.post(
      URL,
      json = payload
    )
    if( resp.status_code != 200 ):
      FBBotSetup._log('Setup Failed...')
    else:
      FBBotSetup._log('=> Success')






  




