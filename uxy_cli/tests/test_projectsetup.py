"""
Authored By Kim Clarence Penaflor
08/11/2019

AWSSetup Test
"""

import os
import json
import unittest
from uxy_cli._generators.proj_setup import ProjSetup


class ProjectSetupTest(unittest.TestCase):
  """
  Project Setup Test
  """

  appConfig = json.loads(open('uxy_cli/tests/testconfig/appconfig.json').read())

  @unittest.skip('temporary skip')
  def test_init_project(self):
    projsetup = ProjSetup(self.appConfig)
    projsetup.clone()

  
  def test_add_config(self):
    projsetup = ProjSetup(self.appConfig)
    projsetup.add_app_config()





