"""
Authored by Kim Clarence Penaflor
08/28/2019
version 0.0.1
Documented via reST

Uxy Component Generator
"""

class ComponentGenerator:
  """
  Generates spiel and unit component
  """

  verbosity = False

  def __init__(self, config):
    """
    Initialize application config
    """

    ComponentGenerator.verbosity = config['verbosity']
    self.config = config

  @classmethod
  def _log(cls, msg):
    """
    Log System Process
    :param msg: string msg to log
    :type msg: string
    """
    if( cls.verbosity ):
      print('[AWS]: ' + msg)

  def generate_spiel(self):
    """
    Generate uxy chatbot spiel
    """



