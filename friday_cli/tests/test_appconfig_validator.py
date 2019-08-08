"""
Authored By Kim Clarence Penaflor
08/08/2019
version 0.0.1

App config validator Test
"""

import json
import unittest
from friday_cli._validators.appconfig_validator import AppConfigValidator


class AppConfigValidatorTest(unittest.TestCase):
  """
  Friday Application Config File unit test
  """

  # Test Application Configuration
  appConfig = json.loads(open('friday_cli/tests/testconfig/appconfig.json').read())
  appConfigFail = json.loads(open('friday_cli/tests/testconfig/appconfig.json').read())

  @unittest.skip("temporary skip..")
  def test_attrib_check(self):
    """
    Test attrib_check
    """
    appconfigValidator = AppConfigValidator(self.appConfig)
    self.assertTrue(appconfigValidator.attrib_check())


  def test_type_check(self):
    """
    Test rule_validation_check
    """


    appconfigValidator = AppConfigValidator(self.appConfig)
    appconfigValidator.rule_validation_check()







