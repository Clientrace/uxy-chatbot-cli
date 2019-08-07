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
  validationRule = {
    'app:name' : {
      'type' : 'string',
      'value' : {
        'set' : 'custom',
        'type' : 'any'
      }
    },
    'app:version' : {
      'type' : 'string',
      'value' : {
        'set' : 'custom',
        'type' : 'numeric'
      }
    },
    'app:description' : {
      'type' : 'string',
      'value' : {
        'set' : 'custom',
        'type' : 'any'
      }
    },
    'runtime' : {
      'type' : 'string',
      'value' : {
        'set' : 'predefined',
        'type' : 'string',
        'lists' : ['python','go']
      }
    }
  }


  def validate(self, appConfig):
    """
    """
    pass



