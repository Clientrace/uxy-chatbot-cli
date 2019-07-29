"""
Authored by Kim Clarence Penaflor
07/30/2019
version 0.0.1
Documented via reST

Load and generate chatbot spiels
"""


import re
import json

global DISPLAY_DIR

DISPLAY_DIR = 'friday_app/chatbot_core/_components/content/'


# Load Display Json
def load_display(userID):
  global DISPLAY_DIR
  display = json.loads(open(DISPLAY_DIR+'displays.json').read())
  return display


# Get Display Spiel
def get_display(userID, displayID):
  displays = load_display(userID)
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


# Quick Reply Response
def quick_reply(userID, displayID, options):
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
  return [{
    'type' : 'btn',
    'data' : text,
    'options' : options,
    'prefix' : '',
    'delay' : 0
  }]



