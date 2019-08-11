"""
Authored By Kim Clarence Penaflor
08/08/2019
version 0.0.1

App config validator Test
"""

import copy
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

  def test_attrib_check(self):
    """
    Test attrib_check
    """
    appconfigValidator = AppConfigValidator(self.appConfig)
    self.assertTrue(appconfigValidator.attrib_check())


  def test_rule_check_valid(self):
    """
    Test rule_validation_check
    """
    print("\nRule Check:")
    config = copy.deepcopy(self.appConfig)
    appconfigValidator = AppConfigValidator(config)
    self.assertTrue(appconfigValidator.rule_validation_check())


  def test_rule_check_appname_invalid(self):
    # Test: config value is empty
    config = copy.deepcopy(self.appConfig)
    config['app:name'] = ''
    appconfigValidator = AppConfigValidator(config)
    self.assertFalse(appconfigValidator.rule_validation_check())
    config = None

  def test_rule_check_appversion_invalid(self):
    # Test: config value invalid type
    config = copy.deepcopy(self.appConfig)
    config['app:version'] = "a"
    appconfigValidator = AppConfigValidator(config)
    self.assertFalse(appconfigValidator.rule_validation_check())
    config = None


  def test_rule_check_region_invalid(self):
    # Test: config invalid option value
    config = copy.deepcopy(self.appConfig)
    config['app:version'] = "a"
    config['aws:config']['region'] = "test"
    appconfigValidator = AppConfigValidator(config)
    self.assertFalse(appconfigValidator.rule_validation_check())
    config = None


  def test_rule_check_chatbotconfig_invalid(self):
    # Test: config invalid option value
    config = copy.deepcopy(self.appConfig)
    config['chatbot:config']['persistent_menu']['call_to_actions'][0] = {
      'type' : 'test',
      'title': 'test',
      'payload' : 'test'
    }
    appconfigValidator = AppConfigValidator(config)
    self.assertFalse(appconfigValidator.rule_validation_check())
    config = self.appConfig.copy()






    







