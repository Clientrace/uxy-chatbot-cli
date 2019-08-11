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

  def test_init_project(self):
    projsetup = ProjSetup(self.appConfig)
    projsetup._clone()


