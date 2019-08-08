"""
Authored By Kim Clarence Penaflor
08/08/2019
version 0.0.1

Application configuration validator
"""

import json


class AppConfigValidator:
  """
  """

  # App config file validation rule:
  validationRule = json.loads(open('friday_cli/_validators/rules/appconfig_rule.json').read())

  def __init__(self, appConfig):
    """
    Initialize App Configuration
    :param appConfig: application config json
    :param type: dictionary
    """
    self.appConfig = appConfig

  @staticmethod
  def _compare_keys(parent, config, dictRule):
    for val in dictRule.keys():
      if( val not in config.keys()):
        return False
    for val in dictRule.keys():
      if( '_rule' not in dictRule[val] ):
        return AppConfigValidator._compare_keys(val, config[val], dictRule[val])
    return True

  def attrib_check(self):
    """
    Check if app config is complete
    :returns: returns whether the app configuration is complete
    :rtype: boolean
    """
    result = AppConfigValidator._compare_keys('root', self.appConfig, AppConfigValidator.validationRule)
    return result

    return True
    # for val in AppConfigValidator.validationRule.keys():
    #   if( val not in self.appConfig ):
    #     return False
      
    # return True

  def type_check(self):
    """
    """
    # for val in AppConfigValidator.validationRule.keys():
    #   if( self.appConfig[val]['type'] )
    pass






