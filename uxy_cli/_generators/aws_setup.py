"""
Authored by Kim Clarence Penaflor
08/05/2019
version 0.0.3
Documented via reST

AWS Development Environment Setup
"""

import os
import time
import json
import uuid
import boto3
import zipfile

class AWSSetup:
  """
  AWS Setup Manager
  """

  verbosity = False

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
    self._s3Client = boto3.client('s3',
     region_name=config['aws:config']['region'])
    self._s3Res = boto3.resource('s3',
     region_name=config['aws:config']['region'])
    self._iamRes = boto3.resource('iam',
     region_name=config['aws:config']['region'])
    self._iamClient = boto3.client('iam',
     region_name=config['aws:config']['region'])
    self._lambda = boto3.client('lambda',
     region_name=config['aws:config']['region'])
    self._dynamodbRes = boto3.resource('dynamodb',
     region_name=config['aws:config']['region'])
    self._dynamodbClient = boto3.client('dynamodb',
     region_name=config['aws:config']['region'])
    self._apiGateway = boto3.client('apigateway',
     region_name=config['aws:config']['region'])
    self._logs = boto3.client('logs',
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


  @staticmethod
  def _init_table(appName, dynamodb, config):
    """
    Initialize Dynamodb Tables
    :param appName: application name
    :param type: string
    :param dynamodb: aws dynamodb instance
    :param type: boto3 object
    :param config: app configuration
    :type config: dictionary
    """

    AWSSetup._log('+ Creating dynamodb session table')

    sessionTableName = appName+'-uxy-session-'+config['app:stage']
    try:
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
      AWSSetup._log('=> Table created')
    except Exception as e:
      if( '(EntityAlreadyExists)' in str(e) ):
        AWSSetup._log('=> Table already exist')

  @staticmethod
  def _create_s3_bucket(appName, _s3, config):
    """
    Creates s3 bucket
    :param appName: application name
    :type appName: string
    :param _s3: aws s3 instance
    :type _s3: boto3 object
    :param config: app configuration
    :type config: dictionary
    :returns: creation status
    :rtype: boolean
    """
    status = False
    s3BucketName = appName+'-uxy-app-'+config['app:stage']
    AWSSetup._log('+ Creating s3 bucket...')
    try:
      _s3.create_bucket(
        Bucket = s3BucketName,
        CreateBucketConfiguration = {
          'LocationConstraint' : config['aws:config']['region']
        }
      )
      status = True
    except Exception as e:
      if( '(OperationAborted)' in str(e) ):
        AWSSetup._log('Bucket name in on queue for deletion.')

    return status


  @staticmethod
  def _save_s3_resource(appName, _s3, contentType, data, config):
    """
    Creates bucket and saves s3 resource data
    :param appName: application name
    :type appName: string
    :param _s3: aws s3 instance
    :type _s3: boto3 object
    :param data: data to save
    :type data: any
    :param config: app configuration
    :type config: dictionary
    """
    s3BucketName = appName+'-uxy-app-'+config['app:stage']
    filename = 'aws_blueprint.json'
    s3Object = _s3.Object(s3BucketName, filename)

    AWSSetup._log('+ Saving app blueprint... ')
    s3Object.put(
      ContentType = contentType,
      Body = data
    )

  @staticmethod
  def _list_s3_objects(bucketName, _s3, config):
    """
    List all s3 objects
    :param bucketName: s3 bucket name
    :type bucketName: string
    :param _s3: aws s3 instance
    :type _s3: boto3 object
    :param config: app configuration
    :type config: dictionary
    """

    s3ObjectList = []
    nextToken = None

    while(True):
      if( nextToken ):
        resp = _s3.list_objects_v2(
          Bucket = bucketName,
          MaxKeys = 10,
          ContinuationToken = nextToken
        )
      else:
        resp = _s3.list_objects_v2(
          Bucket = bucketName,
          MaxKeys = 10
        )

      nextToken = None
      if( resp['IsTruncated'] ):
        nextToken = resp['NextContinuationToken']

      contents = resp['Contents']
      for content in contents:
        s3ObjectList.append({
          'Key' : content['Key']
        })

      if( not nextToken ):
        break

    return s3ObjectList

  @staticmethod
  def _load_s3_text_resource(appName, _s3, resourceName, config):
    """
    :param appName: application name
    :type appName: string
    :param _s3: aws s3 instance
    :type _s3: boto3 object
    :param resourceName: resource to read
    :type resourceName: string
    :param config: app configuration
    :type config: dictionary
    """

    s3BucketName = appName+'-uxy-app-'+config['app:stage']
    s3Object = _s3.Object(s3BucketName, resourceName)
    content = s3Object.get()['Body'].read().decode('utf-8')
    return content

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
  def _compress_app_package(appPackageDir, appPackageDest, ignoreList):
    """
    Compress Folder Directory using ZipFile
    :param appPackageDir: app package directory
    :type appPackageDir: string
    :param appPackageDest: zip file output destination
    :type appPackageDest: string
    """

    if( os.path.isfile(appPackageDest) ):
      os.remove(appPackageDest)
    
    zipf = zipfile.ZipFile(appPackageDest, 'w', zipfile.ZIP_DEFLATED)
    AWSSetup._log('+ Compressing Distributable Package...')
    for root, dirs, files in os.walk(appPackageDir):
      for file in files:
        fDir = os.path.join(root, file)
        # Ignore Git
        ignore = False
        for item in ignoreList:
          if( item in fDir ):
            ignore = True
            break

        if( ignore ):
          continue

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

    if( not os.path.exists(config['app:name']+'/.tmp') ):
      os.mkdir(config['app:name']+'/.tmp')

    if( not os.path.isfile(config['app:name']+'/.tmp/dist.zip') ):
      AWSSetup._compress_app_package(
        config['app:name']+'/.tmp/dist',
        config['app:name']+'/.tmp/dist.zip',
        ['.git/']
      )

    funcName = appName+'-uxy-app-'+config['app:stage']
    zipFile = open(config['app:name']+'/.tmp/dist.zip', 'rb')
    zipFileBin = zipFile.read()
    zipFile.close()

    statusCode = AWSSetup._function_exists(funcName, _lambda)
    if( statusCode == AWSSetup.FUNCTION_NOT_FOUND ):
      runtime = None
      if( config['app:runtime'] == 'go' ):
        runtime = 'go1.x'
      if( config['app:runtime'] == 'python' ):
        runtime = 'python3.6'

      AWSSetup._log("+ Creating lambda function...")
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
  def _update_lambda(appname, _lambda, config):
    """
    Update lambda function
    :param appname: application name
    :type appname: string
    :param _lambda: aws lambda instance
    :type _lambda: boto3 object
    :param config: app configuration
    :type config: dictionary
    """
    if( not os.path.exists('.tmp') ):
      os.mkdir('.tmp')

    if( os.path.isfile('.tmp/dist.zip') ):
      os.remove('.tmp/dist.zip')

    AWSSetup._compress_app_package(
      os.getcwd()+'/.tmp/dist',
      os.getcwd()+'/.tmp/dist.zip',
      ['.git/']
    )
    
    funcName = appname+'-uxy-app-'+config['app:stage']
    zipFile = open('.tmp/dist.zip', 'rb')
    zipFileBin = zipFile.read()
    zipFile.close()

    AWSSetup._log('+ Updating lambda function...')
    response = _lambda.update_function_code(
      FunctionName = funcName,
      ZipFile = zipFileBin
    )
    AWSSetup._log('=> Lambda package deployed')



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
    apiName = appName+'-uxy-app-'+config['app:stage']
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
  def _add_uxy_webhook_method(restApiId, resourceId, httpMethod, lambdaARN,\
     _apiGateway, config, requestTemplates=None):
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

    lambdaMethodURI = 'arn:aws:apigateway:'+config['aws:config']['region']\
      +':lambda:path'\
      + '/2015-03-31/functions/'+lambdaARN+'/invocations'
    if( requestTemplates ):
      response = _apiGateway.put_integration(
        restApiId = restApiId,
        resourceId = resourceId,
        httpMethod = httpMethod,
        type = 'AWS',
        integrationHttpMethod = 'POST',
        uri = lambdaMethodURI,
        requestTemplates = requestTemplates
      )
    else:
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
    response = AWSSetup._generate_apigateway_rest_api(appName, _apiGateway,\
      config)
    restApiId = response['id']

    response = AWSSetup._generate_apigateway_resource(restApiId, 'uxy-webhook',\
      _apiGateway)
    webhookResourceId = response['id']

    fbCallBackMapping = {
      "application/json" : "{\"hub.mode\":\"$input.params('hub.mode')\",\
      \"hub.challenge\":\"$input.params('hub.challenge')\",\
      \"hub.verify_token\":\"$input.params('hub.verify_token')\"}"
    }

    AWSSetup._add_uxy_webhook_method(restApiId, webhookResourceId, 'POST',\
      lambdaARN, _apiGateway, config)

    AWSSetup._put_method_resp(restApiId, webhookResourceId, 'POST', '200',\
       _apiGateway)

    AWSSetup._put_integration_resp(restApiId, webhookResourceId, 'POST', '200',\
       _apiGateway)

    AWSSetup._add_uxy_webhook_method(restApiId, webhookResourceId, 'GET',\
      lambdaARN, _apiGateway, config, fbCallBackMapping)

    AWSSetup._put_method_resp(restApiId, webhookResourceId, 'GET', '200',\
       _apiGateway)

    AWSSetup._put_integration_resp(restApiId, webhookResourceId, 'GET', '200',\
       _apiGateway)

    AWSSetup._log('+ Deploying API...')
    response = AWSSetup._deploy_api(restApiId, _apiGateway, config)
    invokeURL = 'https://'+restApiId+'.execute-api.'\
      +config['aws:config']['region']+'.amazonaws.com/v'\
      +config['app:version']+'/uxy-webhook'

    AWSSetup._log('=> API Deployed')

    return {
      'restApiId' : restApiId,
      'invokeURL' : invokeURL
    }

  @staticmethod
  def _put_integration_resp(restApiId, resourceId, httpMethod, statusCode,\
    _apiGateway):
    """
    Put API Gateway integration response
    :param restApiId: API Gateway rest api Id
    :type restApiId: string
    :param resourceId: API Gateway resource Id
    :type resourceId: string
    :param httpMethod: HTTP Method
    :type httpMethod: string
    :param statusCode: http status
    :type statusCode: string
    :param _apiGateway: API Gateway instance
    :type _apiGateway: boto3 object
    """

    response = _apiGateway.put_integration_response(
      restApiId = restApiId,
      resourceId = resourceId,
      httpMethod = httpMethod,
      statusCode = statusCode,
      responseParameters = {
        "method.response.header.Access-Control-Allow-Origin" : "'*'"
      }
    )
    return response


  @staticmethod
  def _put_method_resp(restApiId, resourceId, httpMethod, statusCode, \
    _apiGateway):
    """
    Put API Gateway integration response
    :param restApiId: API Gateway rest api Id
    :type restApiId: string
    :param resourceId: API Gateway resource Id
    :type resourceId: string
    :param httpMethod: HTTP Method
    :type httpMethod: string
    :param statusCode: http status
    :type statusCode: string
    :param _apiGateway: API Gateway instance
    :type _apiGateway: boto3 object
    """
    response = _apiGateway.put_method_response(
      restApiId = restApiId, 
      resourceId = resourceId,
      httpMethod = httpMethod,
      statusCode = statusCode,
      responseParameters = {
        'method.response.header.Access-Control-Allow-Origin' : False
      },
      responseModels = {
        'application/json' : 'Empty'
      }
    )
    return response

  @staticmethod
  def _get_stream_name(groupname, _logs):
    """
    Get AWS Stream name
    :param groupname: cloudwatch log group name
    :type groupname: string
    :param _logs: cloudwatch instance
    :type _logs: boto3 object
    :returns: log stream name
    :rtype: string
    """
    try:
      resp = _logs.describe_log_streams(
        logGroupName = groupname,
        orderBy = 'LastEventTime',
        descending = True,
        limit = 1
      )
    except Exception as e:
      if( '(ResourceNotFoundException)' in str(e) ):
        print('No application logs yet.')
        return

    return resp['logStreams'][0]['logStreamName']


  @staticmethod
  def _get_log_stream(groupname, _logs):
    """
    Get Log streams
    :param groupname: cloudwatch log group name
    :type groupname: string
    :param _logs: cloudwatch instance
    :type _logs: boto3 object
    :returns: log stream events
    :rtype: dictionary
    """
    stream_name = AWSSetup._get_stream_name(groupname, _logs)
    if( stream_name ):
      resp = _logs.get_log_events(
        logGroupName = groupname,
        logStreamName = stream_name
      )
    else:
      return

    return resp['events']

  def get_logs(self):
    """
    Get cloudwatch events
    """
    groupname = '/aws/lambda/'+self.config['app:name']
    streams = AWSSetup._get_log_stream(groupname, self._logs)
    streamLogs = ''
    if( streams ):
      for stream in streams:
        streamLogs += stream['message'] + '\n'
    return streamLogs

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

  def setup_dynamodb_table(self):
    """
    Setup dynamodb table
    """

    AWSSetup._init_table(self.appName, self._dynamodbRes, self.config)

  def remove_dynamodb_table(self, tableName):
    """
    Remove uxy session table
    """
    response = self._dynamodbClient.delete_table(
      TableName = tableName
    )


  def package_lambda(self, roleARN):
    """
    Setup AWS Lambda
    :param roleARN: AWS IAM Role ARN
    :type roleARN: string
    """

    response = AWSSetup._generate_lambda(self.appName, self._lambda, roleARN, self.config)
    return response['FunctionArn']

  def update_lambda(self):
    """
    Update lambda function code
    """

    try:
      AWSSetup._update_lambda(self.appName, self._lambda, self.config)
    except Exception as e:
      AWSSetup._log(str(e))
      AWSSetup._log("Failed to update application code.")

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

  def setup_s3_bucket(self):
    """
    Setup s3 bucket
    """

    response = AWSSetup._create_s3_bucket(self.appName, self._s3Res, self.config)
    return response

  def save_cloud_config(self, blueprint):
    """
    Save cloud configuration blueprint to s3
    :param blueprint: cloud resource blueprint
    :type blueprint: dictionary
    :returns: aws response
    :rtype: dictionary
    """
    response = AWSSetup._save_s3_resource(self.appName, self._s3Res, 'text/plain', json.dumps(blueprint, indent=2), self.config)
    return response

  def load_cloud_config(self):
    """
    Load cloud configuration file as json
    """
    AWSSetup._log('Loading cloud blueprint...')
    content = AWSSetup._load_s3_text_resource(self.appName, self._s3Res, 'aws_blueprint.json', self.config)
    return json.loads(content)


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

  def detach_iam_policy(self, roleName, policies):
    """
    Detach list of policies in iamrole
    :param roleName: name of role to be detach
    :type roleName: string
    :param policies: list of policy arn
    :type policies: string list
    """
    for policy in policies:
      self._iamClient.detach_role_policy(
        RoleName = roleName,
        PolicyArn = policy
      )

  def get_iam_role(self, roleName):
    """
    Get iam role by name
    :param roleName: iam role name
    :type roleName: string
    :returns: aws response
    :rtype: dictionary
    """
    resp = self._iamClient.get_role(
      RoleName = roleName
    )
    return resp


  def delete_s3_objects(self, bucketName):
    """
    Delete all s3 objects in an s3 bucket
    :param bucketName: name of s3 bucket
    :type bucketName: string
    """

    s3ObjectList = AWSSetup._list_s3_objects(bucketName, self._s3Client, self.config)
    self._s3Client.delete_objects(
      Bucket = bucketName,
      Delete = {
        'Objects' : s3ObjectList
      }
    )

    self._s3Client.delete_bucket(
      Bucket = bucketName
    )




