"""
Authored by Kim Clarence Penaflor
08/01/2019
version 0.0.1
Documented via reST

Facebook API Wrapper
"""


import json
import requests

class Facebook:
  """
  Facebook and Send API Wrapper designed specifically
  for messenger chatbot applications.
  """

  # Facebook API Version
  VERSION = 3.3

  def __init__(self, userID, pageToken):
    """
    Initialize and setup facebook page's access token.
    :param userID: target facebook user's ID
    :param pageToken: generated token for authentication
    :type userID: string
    :type pageToken: string
    """
    self.userID = userID
    self.accessToken = pageToken
    self.hostURL = 'https://graph.facebook.com/v'+str(self.VERSION)
    self.headers = {
      'Content-Type' : 'application/json'
    }

  def http_get(self, route):
    """
    Perform RESTful GET requuest
    :param route: URL route + queryParams
    :type route: string
    :returns: Facebook GET response
    :rtype: JSON body
    """
    queryString = '?' in route and '&' or '?'
    URL = self.hostURL + '/' + route + queryString + 'access_token='+self.accessToken
    resp = requests.get(URL)
    return resp.json()


  def http_post(self, route, payload):
    """
    Perform RESTful POST request
    :param route: Facebook URL endpoint
    :param payload: HTTP POST request payload
    :type route: string
    :type payload: dictionary
    :returns: Facebook POST response
    :rtype: JSON body
    """
    queryString = '?' in route and '&' or '?'
    URL = self.hostURL + '/' + route + queryString + 'access_token='+self.accessToken
    resp = requests.post(
      URL,
      headers = self.headers,
      data = json.dumps(payload)
    )
    return resp.json()

  def get_user_info(self,reqFields):
    """
    Facebook Graph API Get User information
    :param reqFields: information fields to get separated by ',' (ex: first_name, last_name)
    :type reqFields: string
    :returns: Facebook response body 
    :rtype: JSON body
    """
    route = self.userID + '?fields=' + reqFields
    return self.http_get(route)

  def send_txt_msg(self, msg):
    """
    Send Text Message to facebook user
    :param msg: Message to send
    :type msg: string
    :returns: Facebook response body
    :rtype: JSON body
    """
    route = 'me/messages'
    payload = {
      'recipient' : {
        'id' : self.userID
      },
      'message' : {
        'text' : msg
      }
    }
    return self.http_post(route,payload)

  def send_img_msg(self, imgUrl):
    """
    Send Multimedia Image to facebook user
    :param imgUrl: File URL to send
    :type imgUrl: string
    :returns: Facebook response body
    :rtype: JSON body
    """

    route = 'me/messages'
    payload = {
      'recipient' : {
        'id' : self.userID
      },
      'message' : {
        'attachment' : {
          'type' : 'image',
          'payload' : {
            'url' : imgUrl
          }
        }
      }
    }
    return self.http_post(route,payload)

  def send_action(self):
    """
    Sends user typing action
    """
    route = 'me/messages'
    payload = {
      'recipient' : {
        'id' : self.userID
      },
      'sender_action' : 'typing_on'
    }
    return self.http_post(route,payload)

  def send_quick_reply(self, msg, items):
    """
    Sends Quick Options to facebook user
    :param msg: header message in quick reply options
    :type msg: string
    :param items: quick reply options
    :type items: array of quick reply blueprints
    :returns: Facebook POST Response
    :rtype: JSON body
    """
    route = 'me/messages'
    data = []
    for item in items:
      data.append({
        'content_type' : 'text',
        'title' : item,
        'payload' : item
      })

    payload = {
      'recipient' : {
        'id' : self.userID
      },
      'message' : {
        'text' : msg,
        'quick_replies' : data
      }
    }

    return self.http_post(route,payload)

  def send_btn_template(self,buttons,msg):
    """
    Send Button Menu Template
    :param buttons: Menu buttton
    :type buttons: array of button blueprint
    :param msg: button menu header
    :type msg: string
    :returns: Facebook POST Response
    :rtype: JSON body
    """
    route = 'me/messages'
    buttonData = []
    for button in buttons:
      if(list(button)[0]=='postback'):
        buttonData.append({
          'title' : list(button)[1],
          'type' : 'postback',
          'payload' : list(button)[1]
        })

      if(list(button)[0]=='web_url'):
        buttonData.append({
          'title' : list(button)[1],
          'type' : 'web_url',
          'url' :list(button)[2],
          'webview_height_ratio' : list(button)[3].upper(),
          'messenger_extensions' : list(button)[4].lower(),
          'webview_share_button' : 'hide'
        })

    payload = {
      'recipient' : {
        'id' : self.userID
      },
      'message' : {
        'attachment' : {
          'type' : 'template',
          'payload' : {
            'template_type' : 'button',
            'text' : msg,
            'buttons' : buttonData
          }
        }
      }
    }

    return self.http_post(route,payload)


