

from chatbot_core._components import router
from chatbot_core._modules.e2e import resp_builder


def hanlder(event):
  msg_data = event['entry'][0]['messaging'][0]
  userID = msg_data['sender']['id']

  response_data = router.exe(userID, 'facebook', msg_data, None)
  resp_builder.send(userID, 'facebook', response_data)

  return {
    'status' : 200,
    'body' : 'Ok'
  }







