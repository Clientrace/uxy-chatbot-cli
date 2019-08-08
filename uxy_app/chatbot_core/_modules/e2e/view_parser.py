"""
Authored by Kim Clarence Penaflor
07/30/2019
version 0.0.1
Documented via reST
Parse user view from component spiels
"""

import re
import json
from uxy_app.chatbot_core._components import spiel 
from uxy_app.chatbot_core._components import convo_data 
from uxy_app.shared.configuration import config

global VIEW_DIR
VIEW_DIR = 'uxy_app/chatbot_core/_components/view/'


# Get view json
def get_view(sessionName):
  global VIEW_DIR
  viewFile = open(VIEW_DIR+sessionName+'.json').read()
  return json.loads(viewFile)

# Execute view parser and unit output
def exe(userID, sessionName, userInput):
  choices = None
  inputValid = True
  matchedOption = None
  maxRetry = False

  responses = []
  altResponse = []

  view = get_view(sessionName)

  altDisplay = spiel.get_display(userID, "ERR-02")
  if( len(view['opions']) == 0 and len(view['content']) > 0 ):
    displayID = view['content'][-1]
    display = spiel.get_display(userID, displayID)
    altResponse = [{
      'type' : view['optionType'],
      'data' : display['data'],
      'options' : [],
      'prefix' : '',
      'delay' : display['delay']
    }]

  else:
    altResponse = spiel.text(userID, "ERR-01")
    altResponse += [{
      'type' : view['optionType'],
      'data' : altDisplay['data'],
      'options' : view['options'],
      'prefix' : '',
      'delay' : altDisplay['delay']
    }]

  if( userInput != None ):
    if('any' not in view['acceptTypes'] ):
      if( userInput['type'] not in view['acceptTypes'] ):
        inputValid = False

    if( len(view['options']) > 0 and inputValid):
      inputData = None
      if( userInput['type'] == 'payload' ):
        inputData = userInput['data']['payload'].lower()

      if( userInput['type'] == 'text' ):
        inputData = userInput['data']['text'].lower()

      if( userInput['type'] == 'attachment' ):
        inputData = userInput['data']['urls'][0]['payload']['url'].lower()

      optionPos = 0
      if( view['optionType'] == 'quick_reply' or view['optionType'] == 'btn' ):
        for option in view['options']:
          for syn in option['options']:
            if( inputData == syn or ' ' + syn + ' ' in inputData ):
              matchedOption = optionPos
          
          if( matchedOption != None):
            break
          optionPos += 1

      if( matchedOption == None ):
        inputValid = False

    errorLog = int(convo_data.get_item(userID, 'errorLog')) + 1
    if( view['retries'] ):
      if( errorLog >= view['retries'] ):
        maxRetry = True
    
  contents = view['content']
  lastContent = None
  if( len(contents) > 1 and len(view['options']) > 0 ):
    lastContent = contents[-1]
    contents = contents[:len(contents)-1]
    for displayID in contents:
      display = spiel.get_display(userID, displayID)
      responses.append({
        'type' : 'text',
        'data' : display['data'],
        'options' : [],
        'prefix' : '',
        'delay' : display['delay']
      })

  if( view['optionType'] == 'btn' ):
    for option in view['options']:
      if( option['type'] == 'web_url' ):
        matches = re.findall(r"\{{(.*?)\}}", option['url'])
        if( len(matches) > 0 ):
          for match in matches:
            new_val = convo_data.get_item(userID, match)
            option['url'] = option['url'].replace('{{'+match+'}}', new_val)

  if( len(view['options']) == 0 ):
    for displayID in contents:
      display = spiel.get_display(userID, displayID)
      responses.append({
        'type' : 'text',
        'data' : display['data'],
        'options' : [],
        'prefix' : '',
        'delay' : display['delay']
      })

  elif( len(contents) == 1 and lastContent != None ):
    choices = view['options']
    display = spiel.get_display(userID, lastContent)
    responses.append({
      'type' : view['optionType'],
      'data' : display['data'],
      'options' : view['options'],
      'prefix' : '',
      'delay' : display['display']
    })

  elif( len(contents) == 1 ):
    choices = view['options']
    display = spiel.get_display(userID, contents[0])
    responses.append({
      'type' : view['optionType'],
      'data' : display['data'],
      'options' : view['options'],
      'prefix' : '',
      'delay' : display['delay']
    })

  else:
    choices = view['options']
    display = spiel.get_display(userID, lastContent)
    responses.append({
      'type' : view['optionType'],
      'data' : display['data'],
      'options' : view['options'],
      'prefix' : '',
      'delay' : display['delay']
    })

  if( config.environment == 'dev' ):
    state = '[STATE]: ' + sessionName
    responses = spiel.free_text(state, 0) + responses

  return responses, altResponse, choices, matchedOption, inputValid, maxRetry
  

