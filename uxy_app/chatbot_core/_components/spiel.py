"""
Authored by Kim Clarence Penaflor
07/30/2019
version 0.0.1
Documented via reST

Load and generate chatbot spiels
"""

import re
import json
import random

global DISPLAY_DIR
DISPLAY_DIR = 'uxy_app/chatbot_core/_components/content/'


# Load Display Json
def load_display():
  global DISPLAY_DIR
  """
  Load Display Json
  :returns: display json object
  :rtype: json (dictionary)
  """

  display = json.loads(open(DISPLAY_DIR+'displays.json').read())
  return display


# Get Display Spiel
def get_display(userID, displayID):
  displays = load_display()
  if( type(displays[displayID]['data']) == list ):
    displays[displayID]['data'] = random.choice(displays[displayID]['data'])
  return displays[displayID]


# Generate Text Response
def text(userID, displayID):
  display = get_display(userID, displayID)
  return [{
    'type' : 'text',
    'data' : display['text'],
    'options' : [],
    'prefix' : '',
    'delay' : display['delay']
  }]


# Modified Text Response
def mod_text(userID, displayID, key, value):
  display = get_display(userID, displayID)
  return [{
    'type' : 'text',
    'data' : display['data'].replace(key,value),
    'options' : [],
    'prefix' : '',
    'delay' : display['delay']
  }]


# Attachment Response
def display_attachment(url, ftype):
  return [{
    'type' : ftype,
    'data' : url,
    'options' : [],
    'prefix' : '',
    'delay' : 0
  }]


# Free text
def free_text(text, delay):
  """ 
  Generate free text return blueprint

  :type text: string
  :param text: text message to send

  :type delay: integer
  :param delay: message sending action delay

  :returns: Json response blueprint
  :rtype: Json array
  """
  return [{
    'type' : 'text',
    'data' : text,
    'options' : [],
    'prefix' : '',
    'delay' : delay
  }]


# Quick Reply Response
def quick_reply(userID, displayID, options):
  """
  Generate FB quick response blueprint

  :type userID: string
  :param userID: Facebook User ID

  :type displayID: string
  :param displayID: json display ID

  :type options: Json (dictionary) array
  :param options: Quick Reply Buttons

  :returns: Json response blueprint
  :rtype: Json (dictionary) array
  """
  display = get_display(userID, displayID)
  buttons = []
  for option in options:
    buttons.append({
      'data' : option
    })

  return [{
    'type' : 'quick_reply',
    'data' : display['data'],
    'options' : buttons,
    'prefix' : '',
    'delay' : display['delay']
  }]


# Generic Button Template Response
def btn_menu(text, options):
  """ 
  Generate FB Button Template response blueprint
  :type text: string
  :param text: Button menu header

  :type options: Json (dictionary) array
  :param options: array of options

  :returns: Json response blueprint
  :rtype: Json array
  """
  return [{
    'type' : 'btn',
    'data' : text,
    'options' : options,
    'prefix' : '',
    'delay' : 0
  }]



