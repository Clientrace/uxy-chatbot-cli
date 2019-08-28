
from _uxy_core._components import router
from _uxy_core._components import spiel
from _uxy_core._components import convo_data


def exe(userID, data, response, altResponse, choice, optionMatched,\
  valid, maxRetry):
  """
  Execute Unit
  """

  # Catch Invalid User Input
  if( not valid ):
    if( maxRetry ):
      return [], valid

  # Route to next state
  response += router.route(userID, '<ROUTE TO NEXT STATE>')
  return response, valid




