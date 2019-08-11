"""
Chatbot Response Builder
"""

from chatbot_core._modules.e2e.msg_platforms import fb_msg_parser


def send(userID, platform, responseData):
  if( platform == 'facebook' ):
    if( responseData!=None ):
      for response in responseData:
        fb_msg_parser.exe(userID, response)


