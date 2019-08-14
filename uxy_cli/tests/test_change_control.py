"""
Authored By Kim Clarence Penaflor
08/14/2019

AWSSetup Test
"""

import json
import unittest
from uxy_cli._handlers.change_control import ChangeControl


class ChangeControlTest(unittest.TestCase):
  """
  """

  def test_checksum_geneator(self):
    changeControl = ChangeControl('uxy_cli/tests/testconfig/change_control/test_a/')
    checksums = changeControl.generate_filechecksums()
    expected = {
      "uxy_cli/tests/testconfig/change_control/test_a/test.json": "e4781f623a92eb17079aba7702a17ebb",
      "uxy_cli/tests/testconfig/change_control/test_a/level2/test2.json": "3c64bc3f307c64a747c0b78a4dc722f4"
    }
    self.assertTrue(checksums, expected)





