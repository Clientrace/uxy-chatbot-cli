"""
Authored By Kim Clarence Penaflor
08/28/2019

AWSSetup Test
"""

import os.path
import json
import unittest
from uxy_cli._handlers import deployment_handler

class AWSSetupTest(unittest.TestCase):
  """
  Deployment Handler Test
  """

  def test_compile_spiels(self):
    path = os.getcwd()+'/uxy_cli/tests/testconfig/spiels'
    cs = deployment_handler.compile_spiels(path)
    print(cs)



