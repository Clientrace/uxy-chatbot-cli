"""
Authored By Kim Clarence Penaflor
08/08/2019
version 0.0.1

App config validator Test
"""

import json
import unittest
from uxy_cli._validators.appconfig_validator import AppConfigValidator


class AppConfigValidatorTest(unittest.TestCase):
  """
  uxy Application Config File unit test
  """

  # Test Application Configuration
  appConfig = json.loads(open('uxy_cli/tests/testconfig/appconfig.json').read())
  appConfigFail = json.loads(open('uxy_cli/tests/testconfig/appconfig.json').read())

  @unittest.skip("temporary skip..")
  def test_attrib_check(self):
    """
    Test attrib_check
    """
    appconfigValidator = AppConfigValidator(self.appConfig)
    self.assertTrue(appconfigValidator.attrib_check())


  def test_rule_check(self):
    """
    Test rule_validation_check
    """
    print("\nRule Check:")
    config = self.appConfig.copy()
    appconfigValidator = AppConfigValidator(config)
    self.assertTrue(appconfigValidator.rule_validation_check())

    # Test: config value is empty
    config['app:name'] = ''
    appconfigValidator = AppConfigValidator(config)
    self.assertFalse(appconfigValidator.rule_validation_check())

    # Test: config value invalid type
    config = self.appConfig.copy()
    config['app:version'] = "a"
    appconfigValidator = AppConfigValidator(config)
    self.assertFalse(appconfigValidator.rule_validation_check())


    # Test: config invalid option value
    config = self.appConfig.copy()
    config['aws:config']['region'] = "test"
    appconfigValidator = AppConfigValidator(config)
    self.assertFalse(appconfigValidator.rule_validation_check())

    







