"""
Authored By Kim Clarence Penaflor
08/08/2019
version 0.0.1

Application configuration validator
"""

import json
import uxy_cli


class AppConfigValidator:
  """
  """

  # App config file validation rule:
  validationRule = json.loads(open(uxy_cli.ROOT_DIR+'/_validators/rules/appconfig_rule.json').read())

  def __init__(self, appConfig):
    """
    Initialize App Configuration
    :param appConfig: application config json
    :param type: dictionary
    """
    self.appConfig = appConfig

  @staticmethod
  def valid_json(appConfig):
    """
    Checks if the param string is a valid json format
    :param appConfig: application configuration
    :param type: string
    :returns: validation result
    :rtype: boolean
    """
    try:
      json.loads(appConfig)
    except ValueError:
      return False
    return True


  @staticmethod
  def _compare_keys(config, dictRule):
    for val in dictRule.keys():
      if( val not in config.keys()):
        return False

    valid = True
    for val in dictRule.keys():
      if( '_rule' not in dictRule[val] ):
        if( type(dictRule[val]) == list ):
          if( type(config[val]) != list ):
            return False
          for item in config[val]:
            valid = AppConfigValidator._compare_keys(item, dictRule[val][0])
            if( not valid ):
              return valid
        else:
          valid = AppConfigValidator._compare_keys(config[val], dictRule[val])
          if( not valid ):
            return valid
    return True

  @staticmethod
  def _rule_validator(field, val, rule):

    if( rule['type'] == 'integer' ):
      if( type(val) != int ):
        print('[ AppConfig Error ]: '+field+' value must be integer')
        return False

    if( rule['type'] == 'boolean' ):
      if( type(val) != bool ):
        print('[ AppConfig Error ]: '+field+' value must be boolean')
        return False

    if( rule['type'] == 'string' ):
      val = val.strip()
      if( type(val) != str ):
        print('[ AppConfig Error ]: '+field+' value must be string')
        return False
      if( val == '' ):
        print('[ AppConfig Error ]: '+field+' should not be empty')
        return False
      if( rule['value']['type'] == 'numeric' ):
        if( not val.isdigit() ):
          print('[ AppConfig Error ]: '+field+' value should be numeric')
          return False
      if( rule['value']['set'] == 'predefined' ):
        if( val not in rule['value']['lists'] ):
          print('[ AppConfig Error ]: '+field+' should be of the following values: '+str(rule['value']['lists']))
          return False

    return True


  @staticmethod
  def _rule_check(config, dictRule):
    for val in dictRule.keys():
      if( '_rule' in dictRule[val] ):
        valid = AppConfigValidator._rule_validator(val, config[val], dictRule[val]['_rule'])
        if( not valid ):
          return valid

    valid = True
    for val in dictRule.keys():
      if( '_rule' not in dictRule[val] ):
        if( type(dictRule[val]) == list ):
          if( type(config[val]) != list ):
            return False
          for item in config[val]:
            valid = AppConfigValidator._rule_check(item, dictRule[val][0])
            if( not valid ):
              return valid
        else:
          valid = AppConfigValidator._rule_check(config[val], dictRule[val])
          if( not valid ):
            return valid

    return valid


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
    result = AppConfigValidator._rule_check(self.appConfig, AppConfigValidator.validationRule)
    return result


