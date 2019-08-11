"""
Authored by Kim Clarence Penaflor
07/30/2019
version 0.0.1
Documented via reST
"""

import chatbot_core
from chatbot_core.utility.api_wrappers.facebook import Facebook


def parse_string_codes(fb, string_msg):
  if( ':username:' in string_msg ):
    userName = fb.get_user_info('first_name', 'last_name')
    userName = userName['first_name']+' '+userName['last_name']
    string_msg = string_msg.replace(':username:', userName)

  if( ':firstname:' in string_msg ):
    userName = fb.get_user_info('first_name')
    firstName = userName['first_name']
    string_msg = string_msg.replace(':firstname:', firstName)

  return string_msg


def send_text_msg(fb, blueprint):
  fb.send_txt_msg(blueprint['data'])


# TODO Send quick reply
def send_quick_reply():
  pass

# TODO Send Button template
def send_btn_template():
  pass

# TODO Send image multimedia
def send_img():
  pass


def exe(userID, response):
  facebook = Facebook(userID, chatbot_core._environment_.get('FACEBOOK','FB_PAGE_TOKEN'))
  facebook.send_action()

  response['data'] = parse_string_codes(facebook, response['data'])


