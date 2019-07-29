"""
Authored by Kim Clarence Penaflor
07/30/2019
version 0.0.1
Documented via reST
"""


# Get Payload/Postback from inputdata
def _transform_input_payload(inputData):
  if( 'message' in inputData ):
    inputData = inputData['message']
    if('quick_reply' in inputData):
      inputData = inputData['quick_reply']
      return inputData
    return inputData

  if('postback' in inputData):
    return inputData['postback']


# Execute Input Parser
def exe(inputData):
  inputType = None
  parsedInput = {}

  inputData = _transform_input_payload(inputData)

  if( 'attachments' in inputData ):
    inputType = 'attachments'
    parsedInput = {
      'urls' : inputData['attachments']
    }
    if( 'text' in inputData ):
      parsedInput['text'] = inputData['text']

  elif( 'payload' in inputData ):
    inputType = 'payload'
    if( 'text' in inputData ):
      parsedInput = {
        'text' : inputData['text'],
        'payload' : inputData['payload'].strip('_')
      }
    elif( 'title' in inputData ):
      parsedInput = {
        'text' : inputData['title'],
        'payload' : inputData['payload'].strip('_')
      }
    else:
      parsedInput = {
        'payload' : inputData['payload'].strip('_')
      }

  else:
    inputType = 'text'
    parsedInput = {
      'text' : inputData['text']
    }
  
  return {
    'type' : inputType,
    'data' : parsedInput,
    'errors' : 0
  }





