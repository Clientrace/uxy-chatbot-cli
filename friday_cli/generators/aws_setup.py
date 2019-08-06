"""
Authored by Kim Clarence Penaflor
08/05/2019
version 0.0.2
Documented via reST

AWS Development Environment Setup
"""

import os
import json
import uuid
import boto3
import zipfile

class AWSSetup:
  """
  AWS Setup Manager
  APP Config File blueprint:
  {
    'app:name' : <app-name>,
    'app:version' : <app-version>,
    'description' : <app-description>,
    'runtime' : 'python3.6',
    'stage' : <environment stage>,
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
      'lambda:timeout' : 900,
      'iam:roles' : [
        <role1>,
        <role2>
        <role3>
      ]
    },

    'verbosity' : false 
  }
  """

  verbosity = False
  zipPackageDir = '.tmp/fri.zip'
  fridayTemplateDir = 'friday_cli/friday_template'

  # Lambda Function Vars
  FUNCTION_NOT_FOUND = 0
  FUNCTION_FOUND = 1
  FUNCTION_GET_ERROR = 2

  def __init__(self, config):
    """
    Initialize Chatbot App name and configurations
    :param appName: application name
    :type appname: string
    :param config: application configuration
    :type config: dictionary
    """

    AWSSetup.verbosity = config['verbosity']
    self.config = config
    self.appName = config['app:name']

    # Initialize AWS Resources
    self._s3 = boto3.resource('s3')
    self._iamRes = boto3.resource('iam')
    self._iamClient = boto3.client('iam')
    self._lambda = boto3.client('lambda')
    self._dynamodb = boto3.resource('dynamodb')
    self._apiGateway = boto3.client('apigateway')


  @classmethod
  def _log(cls, msg):
    """
    Log System Process
    :param msg: string msg to log
    :type msg: string
    """
    if( cls.verbosity ):
      print(msg)

  # TODO: save app config to s3 bucket
  @staticmethod
  def _save_cloud_config(self):
    pass


  @staticmethod
  def _init_table(appName, dynamodb, config):
    """
    Initialize Dynamodb Tables
    :param appName: application name
    :param type: string
    :param dynamodb: aws dynamodb instance
    :param type: boto3 object
    :param config: app configuration
    :param type
    """
    sessionTableName = appName+'-friday-session-'+config['stage']
    dynamodb.create_table(
      AttributeDefinitions = [{
        'AttributeName' : 'userID',
        'AttributeType' : 'S'
      }],
      ProvisionedThroughput = {
        'ReadCapacityUnits' : config['aws:config']['dynamodb:session-table']['wcu'],
        'WriteCapacityUnits' : config['aws:config']['dynamodb:session-table']['rcu'],
      },
      TableName = sessionTableName,
      KeySchema = [{
        'AttributeName' : 'userID',
        'KeyType' : 'HASH'
      }]
    )


  @staticmethod
  def _generate_iam_role(appName, _iamClient, _iamRes, config):
    """
    Generate IAM Role for chatbot AWS Resources
    :param _iamClient: boto3 iam client instance
    :type _iamClient: boto3 object
    :param _iamRes: boto3 iam resource instance
    :type _iamRes: boto3 object
    :param appName: application name
    :type appname: string
    :param config: application configuration
    :type config: dictionary
    :returns: Role ARN
    :rtype: dictionary
    """

    roleName = appName+'-friday-app'
    AWSSetup._log('+ Creating IAM Role...')
    try:
      _iamClient.create_role(
        RoleName = roleName,
        AssumeRolePolicyDocument = json.dumps({
          'Version' : '2012-10-17',
          'Statement' : [{
            'Effect' : 'Allow',
            'Principal' : {
              'Service' : 'lambda.amazonaws.com'
            },
            'Action' : ['sts:AssumeRole']
          }]
        })
      )
      apiRole = _iamRes.Role(roleName)
      roleArn = apiRole.arn
      for role in config['iamRoles']:
        AWSSetup._log('+ Attaching Role: '+role+'...')
        apiRole.attach_policy(
          PolicyArn = role
        )
      
      apiRole.reload()
      AWSSetup._log('==> Role Created.')
    except Exception as e:
      if( '(EntityAlreadyExists)' in str(e) ):
        apiRole = _iamRes.Role(roleName)
        roleArn = apiRole.arn
        AWSSetup._log('==> Role Created.')

    AWSSetup._log('=> Role ARN: '+str(roleArn))
    return roleArn

  @staticmethod
  def _compress_app_package(appPackageDir, appPackageDest):
    """
    Compress Folder Directory using ZipFile
    :param appPackageDir: app package directory
    :type appPackageDir: string
    :param appPackageDest: zip file output destination
    :type appPackageDest: string
    """

    zipf = zipfile.ZipFile(appPackageDest, 'w', zipfile.ZIP_DEFLATED)
    AWSSetup._log('+ Compressing Template...')
    for root, dirs, files in os.walk(appPackageDir):
      for file in files:
        fDir = os.path.join(root, file)
        zipf.write(
          filename = fDir,
          arcname = fDir.replace(appPackageDir,'')
        )


  @staticmethod
  def _function_exists(funcName, _lambda):
    """
    Check if lambda function exist
    :param funcName: lambda function resource name
    :type funcName: string
    :param _lambda: aws lambda client controller
    :type _lambda: boto3 client object
    :returns: status code (FUNCTION_FOUND | FUNCTION_NOT_FOUND | FUNCTION_GET_ERROR)
    :rtype: integer
    """

    try:
      _lambda.get_function(
        FunctionName = funcName
      )
      return AWSSetup.FUNCTION_FOUND
    except Exception as e:
      if( '(ResourceNotFoundException)' in str(e) ):
        return AWSSetup.FUNCTION_NOT_FOUND
    return AWSSetup.FUNCTION_GET_ERROR

  @staticmethod
  def _generate_lambda(appName, _lambda, roleARN, config):
    """
    Creates AWS lambda function and uploads app template
    :param appName: application name
    :type appName: string
    :param _lambda: boto3 lambda client instance
    :type _lambda: boto3 object
    :param roleARN: IAM Role
    :type roleARN: string
    :param config: application configuration
    :returns: aws response
    :rtype: dictionary
    """

    funcName = appName+'-friday-app-'+config['stage']
    AWSSetup._compress_app_package(
      AWSSetup.fridayTemplateDir,
      AWSSetup.zipPackageDir
    )

    zipFile = open(AWSSetup.zipPackageDir,'rb')
    zipFileBin = zipFile.read()
    zipFile.close()

    statusCode = AWSSetup._function_exists(funcName, _lambda)
    if( statusCode == AWSSetup.FUNCTION_NOT_FOUND ):
      AWSSetup._log('+ Creating lambda function...')
      response = _lambda.create_function(
        FunctionName = funcName,
        Runtime = config['runtime'],
        Role = roleARN,
        Handler = config['aws:config']['lambda:handler'],
        Code = {
          'ZipFile' : zipFileBin
        },
        Timeout = config['aws:config']['lambda:timeout']
      )
    elif ( statusCode == AWSSetup.FUNCTION_FOUND ):
      AWSSetup._log('+ Updating lambda function...')
      response = _lambda.update_function_code(
        FunctionName = funcName,
        ZipFile = zipFileBin
      )
    else:
      AWSSetup._log('==> ERROR: error getting lambda function')
      response = {}

    return response

  @staticmethod
  # TODO: API Gateway Generator
  def _generate_api_gateway(appName, _apiGateway, config):
    apiName = appName+'-friday-app-'+config['stage']
    response = _apiGateway.create_rest_api(
      name = apiName,
      description = config['app:description'],
      version = config['app:version'],
      endpointConiguration = {
        'types' : [
          'REGIONAL'
        ]
      }
    )

  def remove_iamrole(self, roleName):
    """
    Deletes AWS IAM Role
    :param roleName: AWS Rolename
    :type roleName: string
    :returns: boto3 aws response
    :rtype: dictionary
    """

    response = self._iamClient.delete_role(
      RoleName = roleName
    )

    return response

  def setup_iamrole(self):
    """
    Setup AWS Role
    :returns: Role ARN
    :rtype: string
    """

    ARN = AWSSetup._generate_iam_role(self.appName, self._iamClient, self._iamRes, self.config)
    return ARN

  def remove_lambda(self, funcName):
    """
    Remove AWS lambda function
    :param funcName: aws lambda function name
    :type funcName: string
    :returns: boto3 aws response
    :rtype: dictionary
    """

    try:
      response = self._lambda.delete_function(
        FunctionName = funcName
      )
    except Exception as e:
      response = {}

    return response


  def package_lambda(self, roleARN):
    """
    Setup AWS Lambda
    :param roleARN: AWS IAM Role ARN
    :type roleARN: string
    """

    response = AWSSetup._generate_lambda(self.appName, self._lambda, roleARN, self.config)
    return response




