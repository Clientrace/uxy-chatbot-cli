"""
Authored By Kim Clarence Penaflor
08/06/2019
version 0.0.1

AWSSetup Test
"""

import os.path
import json
import unittest
from uxy_cli._generators.aws_setup import AWSSetup

class AWSSetupTest(unittest.TestCase):
  """
  AWS Setup unit test
  """

  # Test Application Configuration
  appConfig = json.loads(open('uxy_cli/tests/testconfig/appconfig.json').read())

  @unittest.skip('Skip')
  def test_iamrole_generator(self):
    """
    Test iamRole generator
    """
    # Generate IAM Role
    awsSetup = AWSSetup(self.appConfig)
    ARN = awsSetup.setup_iamrole()

    self.assertTrue( ARN != None )
    self.assertTrue( 'testbot-uxy-app' in ARN )

    # Remove Generated ARN
    resp = awsSetup.remove_iamrole('testbot-uxy-app')
    self.assertTrue( 
      resp['ResponseMetadata']['HTTPStatusCode'], 200
    )



  @unittest.skip('Skip')
  def test_package_compression(self):
    """
    Test Zip compressor
    """
    appPackageDir = 'uxy_cli/project_template'
    appPackageDest = '.tmp/test.zip'

    # Removes Initial File
    if( os.path.isfile(appPackageDest) ):
      os.remove(appPackageDest)
    AWSSetup._compress_app_package(appPackageDir, appPackageDest)
    self.assertTrue( os.path.isfile(appPackageDest) )
    os.remove(appPackageDest)


  @unittest.skip('Skip')
  def test_lambda_generator(self):
    """
    Test lambda generator (Function Create)
    """

    awsSetup = AWSSetup(self.appConfig)
    awsSetup.remove_lambda('testbot-uxy-app')

    # Test Lambda Create
    iamRoleARN = awsSetup.setup_iamrole()
    resp = awsSetup.package_lambda(iamRoleARN)
    self.assertTrue(
      resp['ResponseMetadata']['HTTPStatusCode'], 201
    )

    # Test Lambda Update
    resp = awsSetup.package_lambda(iamRoleARN)
    self.assertTrue(
      resp['ResponseMetadata']['HTTPStatusCode'], 200
    )

    awsSetup.remove_iamrole('testbot-uxy-app')
    awsSetup.remove_lambda('testbot-uxy-app')

  def test_apigateway_create_rest(self):
    """
    Test API Gateway Rest API Generator
    """

    # print('Uxygen Test')
    awsSetup = AWSSetup(self.appConfig)
    iamRoleARN = awsSetup.setup_iamrole()

    resp = awsSetup.package_lambda(iamRoleARN)
    lambdaARN = resp['FunctionArn']

    awsSetup._add_uxy_webhook_method('fkci9kzuhj','uh98h1','POST',lambdaARN, awsSetup._apiGateway, self.appConfig)


    # resp = awsSetup.setup_uxy_api(lambdaARN)
    # restApiId = resp['restApiId']

    # awsSetup.delete_apigateway_rest(restApiId)
    # awsSetup.remove_iamrole('testbot-uxy-app')
    # awsSetup.remove_lambda('testbot-uxy-app')

    

if __name__ == '__main__':
  unittest.main()




