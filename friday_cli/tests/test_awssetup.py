"""
Authored By Kim Clarence Penaflor
08/06/2019
version 0.0.1

AWSSetup Test
"""

import os.path
import json
import unittest
from friday_cli.generators.aws_setup import AWSSetup

class AWSSetupTest(unittest.TestCase):
  """
  AWS Setup unit test
  """

  # Test Application Configuration
  appConfig = {
    'app:name' : 'testbot',
    'app:version' : 1,
    'description' : 'test chatbot',
    'runtime' : 'python3.6',
    'stage' : 'dev',
    'aws:config' : {
      'dynamodb:session-table' : {
        'wcu' : 5,
        'rcu' : 5
      },
      'dynamodb:auth-table' : {
        'wcu' : 5,
        'rcu' : 5
      },
      'lambda:handler' : 'index.lambda_handler',
      'lambda:timeout' : 900
    },
    'verbosity' : False
  }

  @unittest.skip('Temporary Skip..')
  def test_iamrole_generator(self):
    """
    Test iamRole generator
    """
    # Generate IAM Role
    awsSetup = AWSSetup(self.appConfig)
    ARN = awsSetup.setup_iamrole()

    self.assertTrue( ARN != None )
    self.assertTrue( 'testbot-friday-app' in ARN )

    # Remove Generated ARN
    resp = awsSetup.remove_iamrole('testbot-friday-app')
    self.assertTrue( 
      resp['ResponseMetadata']['HTTPStatusCode'], 200
    )


  @unittest.skip('Temporary Skip..')
  def test_package_compression(self):
    appPackageDir = 'friday_cli/friday_template'
    appPackageDest = '.tmp/test.zip'

    # Removes Initial File
    if( os.path.isfile(appPackageDest) ):
      os.remove(appPackageDest)
    AWSSetup._compress_app_package(appPackageDir, appPackageDest)
    self.assertTrue( os.path.isfile(appPackageDest) )
    os.remove(appPackageDest)


  @unittest.skip('Temporary Skip..')
  def test_lambda_generator(self):
    """
    Test lambda generator
    """
    awsSetup = AWSSetup(self.appConfig)

    iamRoleARN = awsSetup.setup_iamrole()
    response = awsSetup.setup_lambda(iamRoleARN)


if __name__ == '__main__':
  unittest.main()





