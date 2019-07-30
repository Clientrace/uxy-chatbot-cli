import unittest
from unittest.mock import patch
from friday_app.chatbot_core._modules.e2e import view_parser


class TestViewPaser(unittest.TestCase):
  def test_get_view(self):
    result = view_parser.get_view('welcome')
    self.assertEqual(result,{
      'acceptTypes' : ['any'],
      'content' : ['FS-02'],
      'optionType' : 'text',
      'options' : [],
      'retries' : None
    })

  def text_view_text(self):
    pass

        
