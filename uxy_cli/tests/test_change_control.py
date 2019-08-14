"""
Authored By Kim Clarence Penaflor
08/14/2019

ChangeControl Test
"""

import json
import unittest
from uxy_cli._handlers.change_control import ChangeControl


class ChangeControlTest(unittest.TestCase):
  """
  """

  appConfig = json.loads(open('uxy_cli/tests/testconfig/appconfig.json').read())

  def init_test_files(self):
    testFileContent = {
      'sample' : 'sample',
      'sample2' : 'sample',
      'sample3' : 'sample',
      'sample4' : 'sample'
    }
    testFileContent2 = {
      'sample5' : 'sample',
      'sample6' : 'sample',
      'sample7' : 'sample',
      'sample8' : 'sample'
    }
    testfile = open('uxy_cli/tests/testconfig/change_control/test_a/test.json','w')
    testfile.write(json.dumps(testFileContent,indent=4))
    testfile.close()

    testfile2 = open('uxy_cli/tests/testconfig/change_control/test_a/level2/test2.json','w')
    testfile2.write(json.dumps(testFileContent2,indent=4))
    testfile2.close()

  def test_checksum_generator(self):
    changeControl = ChangeControl('uxy_cli/tests/testconfig/change_control/test_a/',self.appConfig)
    checksums = changeControl.generate_filechecksums()
    expected = {
      "uxy_cli/tests/testconfig/change_control/test_a/test.json": "e4781f623a92eb17079aba7702a17ebb",
      "uxy_cli/tests/testconfig/change_control/test_a/level2/test2.json": "3c64bc3f307c64a747c0b78a4dc722f4"
    }
    self.assertTrue(checksums, expected)


  def test_diff_comparison(self):
    # Modify Files
    testFileContent = {
      'sample' : 'sample',
      'sample2' : 'sample',
      'sample3' : 'sample',
      'sample4' : 'sample'
    }
    testFile = open('uxy_cli/tests/testconfig/change_control/test_a/test.json')

    


