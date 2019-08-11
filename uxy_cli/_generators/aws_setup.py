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
    'app:description' : <app-description>,
    'app:runtime' : 'python3.6',
    'app:stage' : <environment stage>,
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
  zipPackageDir = '.tmp/dist.zip'
  uxyTemplateDir = 'uxy_cli/project_template/dist_template/'

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
    self._s3 = boto3.resource('s3',
     region_name=config['aws:config']['region'])
    self._iamRes = boto3.resource('iam',
     region_name=config['aws:config']['region'])
    self._iamClient = boto3.client('iam',
     region_name=config['aws:config']['region'])
    self._lambda = boto3.client('lambda',
     region_name=config['aws:config']['region'])
    self._dynamodb = boto3.resource('dynamodb',
     region_name=config['aws:config']['region'])
    self._apiGateway = boto3.client('apigateway',
     region_name=config['aws:config']['region'])


  @classmethod
  def _log(cls, msg):
    """
    Log System Process
    :param msg: string msg to log
    :type msg: string
    """
    if( cls.verbosity ):
      print('[AWS]: ' + msg)

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
    sessionTableName = appName+'-uxy-session-'+config[app:stage]
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

    roleName = appName+'-uxy-app'
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
      for role in config['aws:config']['iam:roles']:
        AWSSetup._log('+ Attaching Role: '+role+'...')
        apiRole.attach_policy(
          PolicyArn = role
        )
      
      apiRole.reload()
      AWSSetup._log('=> Role Created.')
    except Exception as e:
      if( '(EntityAlreadyExists)' in str(e) ):
        apiRole = _iamRes.Role(roleName)
        roleArn = apiRole.arn
        AWSSetup._log('=> Role Created.')
      else:
        print(str(e))

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
  def _get_lambda_function(funcName, _lambda):
    """
    Check if lambda function exist
    :param funcName: lambda function resource name
    :type funcName: string
    :param _lambda: aws lambda client controller
    :type _lambda: boto3 client object
    :returns: aws response
    :rtype: dictionary
    """
    result = _lambda.get_function(
      FunctionName = funcName
    )
    return result

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
      AWSSetup._get_lambda_function(funcName, _lambda)
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

    funcName = appName+'-uxy-app-'+config[app:stage]
    AWSSetup._compress_app_package(
      AWSSetup.uxyTemplateDir,
      AWSSetup.zipPackageDir
    )

    zipFile = open(AWSSetup.zipPackageDir,'rb')
    zipFileBin = zipFile.read()
    zipFile.close()

    statusCode = AWSSetup._function_exists(funcName, _lambda)
    if( statusCode == AWSSetup.FUNCTION_NOT_FOUND ):
      runtime = None
      if( config['app:runtime'] == 'go' ):
        runtime = 'go1.x'
      if( config['app:runtime'] == 'python' ):
        runtime = 'python3.6'

      AWSSetup._log('+ Creating lambda function...')
      response = _lambda.create_function(
        FunctionName = funcName,
        Runtime = runtime,
        Role = roleARN,
        Handler = config['aws:config']['lambda:handler'],
        Code = {
          'ZipFile' : zipFileBin
        },
        Timeout = config['aws:config']['lambda:timeout']
      )
      AWSSetup._log("=> Lambda package deployed")
    elif ( statusCode == AWSSetup.FUNCTION_FOUND ):
      AWSSetup._log('+ Updating lambda function...')
      response = _lambda.update_function_code(
        FunctionName = funcName,
        ZipFile = zipFileBin
      )
      AWSSetup._log("=> Lambda package deployed")
    else:
      AWSSetup._log('=> ERROR: error getting lambda function')
      response = {}


    return response


  @staticmethod
  def _get_apigateway_rootId(restApiId, _apiGateway):
    """
    Get API Gateway Rest API Root [/] ID
    :param restApiId: AWS API Gateway Rest API ID
    :type restApiId: string
    :param _apiGateway: API Gateway instance
    :type _apiGateway: boto3 object
    :returns: rest api root id
    :rtype: string
    """

    response = _apiGateway.get_resources(
      restApiId = restApiId,
      embed = ['/']
    )
    return response['items'][0]['id']

  @staticmethod
  def _deploy_api(restApiId, _apiGateway, config):
    """
    Deploy uxy Rest API
    :param restApiId: AWS API Gateway Rest API ID
    :type restApiId: string
    :param _apiGateway: API Gateway instance
    :type _apiGateway: boto3 object
    """
    # Create Deployment
    _apiGateway.create_deployment(
      restApiId = restApiId,
      stageName = 'v'+config['app:version']
    )

    response = _apiGateway.get_stage(
      restApiId = restApiId,
      stageName = 'v'+config['app:version']
    )

    return response


  @staticmethod
  def _generate_apigateway_resource(restApiId, pathPart, _apiGateway):
    """
    Create AWS API Gateway Rest Resource
    :param restApiId: AWS API Gateway Rest API ID
    :type restApiId: string
    :param pathPart: rest path
    :param _apiGateway: API Gateway instance
    :type _apiGateway: boto3 object
    :param config: app configuration
    :type config: dictionary
    :returns: rest api root id
    :rtype: string
    """
    rootResourceId = AWSSetup._get_apigateway_rootId(restApiId, _apiGateway)
    response = _apiGateway.create_resource(
      restApiId = restApiId,
      parentId = rootResourceId,
      pathPart = pathPart
    )
    return response


  @staticmethod
  def _generate_apigateway_rest_api(appName, _apiGateway, config):
    """
    Create AWS API Gateway Rest API
    :param appName: application name
    :type appName: string
    :param _apiGateway: api gateway instance
    :type _apiGateway: boto3 object
    :param config: app configuration
    :type config: dictionary
    :returns: aws response
    :rtype: dictionary
    """
    apiName = appName+'-uxy-app-'+config[app:stage]
    response = _apiGateway.create_rest_api(
      name = apiName,
      description = config['app:description'],
      version = config['app:version'],
      endpointConfiguration = {
        'types' : [
          'REGIONAL'
        ]
      }
    )
    return response

  @staticmethod
  def _add_uxy_webhook_method(restApiId, resourceId, httpMethod, lambdaARN, _apiGateway, config):
    """
    Add uxy App API Resource for FB Webhook
    :param restApiId: aws api gateway rest api id
    :type restApiId: string
    :param resourceId: api resource id
    :type resourceId: string
    :param httpMethod: HTTP Method
    :type httpMethod: string
    :param lambdaARN: aws lambda resource name
    :type lambdaARN: string
    :param _apiGateway: api gateway instance
    :type _apiGateway: boto3 object
    :param config: app configuration
    :type config: dictionary
    :returns: aws response
    :rtype: dictionary
    """

    _apiGateway.put_method(
      restApiId = restApiId,
      resourceId = resourceId,
      httpMethod = httpMethod,
      authorizationType = 'NONE'
    )

    lambdaMethodURI = 'arn:aws:apigateway:'+config['aws:config']['region']+':lambda:path'\
      + '/2015-03-31/functions/'+lambdaARN+'/invocations'
    response = _apiGateway.put_integration(
      restApiId = restApiId,
      resourceId = resourceId,
      httpMethod = httpMethod,
      type = 'AWS',
      integrationHttpMethod = 'POST',
      uri = lambdaMethodURI
    )
    return response

  @staticmethod
  def _generate_uxy_api(appName, _apiGateway, lambdaARN, config):
    """
    Generate uxy API
    :param appName: application name
    :type appName: string
    :param _apiGateway: api gateway instance
    :type _apiGateway: boto3 object
    :param lambdaARN: aws lambda resource name
    :type lambdaARN: string
    :param config: app configuration
    :type config: dictionary
    :returns: rest api id and invocation url
    :rtype: dictionary
    """

    AWSSetup._log('+ Generating Rest API...')
    response = AWSSetup._generate_apigateway_rest_api(appName, _apiGateway, config)
    restApiId = response['id']

    response = AWSSetup._generate_apigateway_resource(restApiId, 'uxy-webhook', _apiGateway)
    webhookResourceId = response['id']

    print('WEBHOOK RESOURCE ID: ')
    print(webhookResourceId)

    AWSSetup._add_uxy_webhook_method(restApiId, webhookResourceId, 'POST', lambdaARN, _apiGateway, config)

    AWSSetup._log('+ Deploying API...')
    response = AWSSetup._deploy_api(restApiId, _apiGateway, config)
    invokeURL = 'https://'+restApiId+'execute-api.'+config['aws:config']['region']+'.amazonaws.com/'+config['app:version']

    AWSSetup._log('=> API Deployed')

    return {
      'restApiId' : restApiId,
      'invokeURL' : invokeURL
    }

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

  def setup_uxy_api(self, lambdaARN):
    """
    Setup AWS uxy App API Gateway RestAPI
    :param lambdaARN: aws lambda resource name
    :type lambdaARN: string
    :returns: api invocation url
    :rtype: string
    """

    response = AWSSetup._generate_uxy_api(self.appName, self._apiGateway, lambdaARN, self.config)
    return response

  def delete_apigateway_rest(self, restApiId):
    """
    Get AWS API Gateway Rest API
    :param restApiId: rest api id
    :type restApiId: string
    :param _apiGateway: api gateway instance
    :type _apiGateway: boto3 object 
    :returns: aws response
    :rtype: dictionary
    """

    response = self._apiGateway.delete_rest_api(
      restApiId = restApiId
    )
    return response


