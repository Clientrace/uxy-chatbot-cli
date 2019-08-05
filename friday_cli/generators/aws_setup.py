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


class AWSSetup:
  """
  AWS Setup Manager
  """

  def __init__(self, appName, config):
    """
    Initialize Chatbot App name and configurations
    :param appName: applicatiton name
    :param type: string
    :param config: application configuration
    :param type: dictionary
    """

    self.appName = appName
    self.config = config

    # Initialize AWS Resources
    self._dynamodb = botto3.resource('dynamodb')
    self._s3 = boto3.resource('s3')
    self._IAMRes = boto3.resource('iam')
    self._IAMClient = boto3.client('iam')

  def _log(self, msg):
    """
    Log System Process
    :param string: string msg to log
    :param type: string
    """
    if( self.verbosity ):
      print(msg)

  # TODO: save app config to s3 bucket
  @staticmethod
  def _save_cloud_config(self):
    pass


  # TODO: Dynamobd Init
  @staticmethod
  def _init_table(self):
    pass

  @staticmethod
  def _generate_iam_role(iamClient, iamRes, appName, config):
    """
    Generate IAM Role for chatbot AWS Resources
    :param iamClient: boto3 iam client instance
    :param type: boto3 class
    :param iamRes: boto3 iam resource instance
    :param type: boto3 class
    :param appName: application name
    :param type: string
    :param config: app config
    :param type: dictionary
    :returns: Role ARN
    :rtype: dictionary
    """

    roleName = appName+'friday-app'
    try:
      iamClient.create_role(
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
      apiRole = iamRes.Role(roleName)
      for role in config['iamRoles']:
        self._log('+ Attaching Role: '+role+'.')
        apiRole.attach_policy(
          PolicyArn = role
        )
      
      apiRole.reload()
      self._log('==> Role Created.')
    except Exception as e:
      if( '(EntityAlreadyExists)' in str(e) ):
        apiRole = iamRes.Role(roleName)
        roleArn = apiRole.arn
        self._log('==> Role Created.')

    self._log('Role ARN: '+str(roleArn))
    return roleArn


    





  





