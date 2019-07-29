"""
Authored by Kim Clarence Penaflor
07/30/2019
version 0.0.1
Documented via reST
Parse user view from component spiels
"""


import re
import json
from friday_app.chatbot_core._components import spiel
from friday_app.chatbot_core._components import convo_data
from friday_app.shared.configration import config

global VIEW_DIR
VIEW_DIR = 'friday_app/chatbot_core/_components/view/'


# Get view json
def get_view(sessionName):
  global VIEW_DIR
  viewFile = open(VIEW_DIR+sessionName+'.json').read()
  return json.loads(viewFile)

# Execute view parser and unit output
# TODO View Parser Exe
def exe(userID, sessionName, userInput):
  pass





