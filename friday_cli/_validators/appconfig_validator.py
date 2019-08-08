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
  def _compare_keys(config, dictRule):
    for val in dictRule.keys():
      if( val not in config.keys()):
        return False

    for val in dictRule.keys():
      if( '_rule' not in dictRule[val] ):
        return AppConfigValidator._compare_keys(config[val], dictRule[val])
    return True

  @staticmethod
  def _rule_validator(val, rule):
    if( rule['type'] == 'string' ):
      if( type(val) != str ):
        return False

    if( rule['type'] == 'integer' ):
      if( type(val) != int ):
        return False

    if( rule['type'] != 'boolean' ):
      if( type(val) != bool ):
        return False

    if( rule['value']['set'] == 'predefined' ):
      if( val not in rule['value']['lists'] ):
        return False

    if( rule['value']['type'] == 'numeric' ):
      if( not val.isdigit() ):
        return False

    return True


  @staticmethod
  def _type_check(config, dictRule):
    for val in dictRule.keys():
      if('_rule' in dictRule[val]):
        AppConfigValidator._rule_validator(val, dictRule[val]['_rule'])

    for val in dictRule.keys():
      if( '_rule' not in dictRule[val] ):
        return AppConfigValidator._type_check(config[val], dictRule[val])

    return True


  def attrib_check(self):
    """
    Check if app config is complete
    :returns: validation result
    :rtype: boolean
    """
    result = AppConfigValidator._compare_keys(self.appConfig, AppConfigValidator.validationRule)
    return result


  def rule_validation_check(self):
    """
    Check if app follows the validation rule
    :returns: validation result
    :rtype: boolean
    """
    result = AppConfigValidator._type_check(self.appConfig, AppConfigValidator.validationRule)
    return result




