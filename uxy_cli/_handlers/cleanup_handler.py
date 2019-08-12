"""
Authored by Kim Clarence Penaflor
08/12//2019
version 0.0.2
Documented via reST

Project uxy cli clueanup handler module
"""

import json
import os


def purge():
  # Load uxy configuration file
  if( not os.path.isfile('uxy.json') ):
    print('Failed to locate app configuration file..')

  pass





