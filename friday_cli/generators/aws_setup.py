"""
Authored by Kim Clarence Penaflor
08/05/2019
version 0.0.2
Documented via reST

AWS Development Environment Setup
"""


import boto3
import uuid
import json
import zipfile


class AWSSetup:
  """
  AWS Setup Manager
  """

  verbosity = False

  def __init__(self, appName, config):
    """
    Initialize Chatbot App name and configurations
    :param appName: applicatiton name
    :type appname: string
    :param config: application configuration
    :type config: dictionary
    """

    """
    config blueprint:
    {
      'app' : <app-name>,
      'stage' : <environment stage>,
      'environments' : {
        'production' : {
          'replace' : <default.env.file.cfg>,
          'with' : <prod.env.file.cfg>
        },
        'development' : {
          'replace' : <default.env.file.cfg>,
          'with' : <dev.env.file.cfg>
        }
      },
      'aws:configs' : {
        'dynamodb:session-table' : {
          'wcu' : 5,
          'rcu' : 5
        },
        'dynamodb:auth-table' : {
          'wcu' : 5,
          'rcu' : 5
        }
      },
      'verbosity' : false 
    }
    """

    self.appName = appName
    self.config = config

    # Initialize AWS Resources
    self._dynamodb = boto3.resource('dynamodb')
    self._s3 = boto3.resource('s3')
    self._IAMRes = boto3.resource('iam')
    self._IAMClient = boto3.client('iam')
    self.verbosity = config['verbosity']

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
    sessionTableName = appName+'friday-session-'+config['stage']
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
    :type _iamClient: boto3 class
    :param _iamRes: boto3 iam resource instance
    :type _iamRes: boto3 class
    :param appName: application name
    :type appname: string
    :param config: app config
    :type config: dictionary
    :returns: Role ARN
    :rtype: dictionary
    """

    roleName = appName+'friday-app'
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
      for role in config['iamRoles']:
        AWSSetup._log('+ Attaching Role: '+role+'.')
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

    AWSSetup._log('Role ARN: '+str(roleArn))
    return roleArn


  @staticmethod
  # TODO AWS Lambda generator (zipper)
  def _create_function(appName, _lambda, roleARN, config):
    zipFileName = 'frApp.zip'
    with zipFile.ZipFile(zipFileName, 'a') as file:
      pass


  def setup(self):
    AWSSetup._create_function(self.appName,'test','test',self.config)







