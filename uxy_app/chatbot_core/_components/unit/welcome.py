
from uxy_app.chatbot_core._components import router
from uxy_app.chatbot_core._components import spiel
from uxy_app.chatbot_core._components import convo_data



def exe(userID, data, response, altResponse, choice, optionMatched, valid ,maxRetry):
  # Comment out for input validation
  # if( not valid ):
  #   if( maxRetry ):
  #     return [], valid


  response += router.route(userID, 'main')
  return response, valid
  


