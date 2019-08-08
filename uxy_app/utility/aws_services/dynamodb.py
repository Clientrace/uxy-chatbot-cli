"""
Authored by Kim Clarence Penaflor
08/01/2019
version 0.0.1
Documented via reST

AWS Dynamodb Controller
"""


import boto3


class Dynamodb:
  """
  Dynamodb SDK Controller
  """

  def __init__(self, tableName, awsCred=None):
    """
    Initialize Dynamodb Table
    :param tableName: AWS Dynamodb Tablename
    :param awsCred: AWS Credentials (id and secret token)
    :type tableName: string
    :type awsCred: Dictionary {'aws_id': '<aws ID>', 'aws_secret' : '<aws secret token'}
    """
    self.tableName = tableName

    # Init DB Table With custom awscred
    if(awsCred):
      self.DYNAMODB_c = boto3.client(
        'dynamodb',
        aws_access_key_id = awsCred['aws_id'],
        aws_secret_access_key = awsCred['aws_secret'],
        region_name = 'ap-southeast-1'
      )
      self.DYNAMODB_r = boto3.resource(
        'dynamodb',
        aws_access_key_id = awsCred['aws_id'],
        aws_secret_access_key = awsCred['aws_secret'],
        region_name = 'ap-southeast-1'
      )
    # Regular Initialization
    else:
      self.DYNAMODB_c = boto3.client(
        'dynamodb',
        region_name = 'ap-southeast-1'
      )
      self.DYNAMODB_r = boto3.resource(
        'dynamodb',
        region_name = 'ap-southeast-1'
      )
      

  def put_item(self, item):
    """
    Dynamodb Add record
    :param item: Dynamodb Item
    :type item: json (dictionary)
    :returns: Dynamodb Response object
    :rtype: json (dictionary)
    """

    resp = self.DYNAMODB_c.put_item(
      TableName = self.tableName,
      Item = item,
      ReturnConsumedCapacity = 'TOTAL'
    )
    return resp

  def update_item(self, key, item):
    """
    Dynamodb update item attribute
    :param key: Item key
    :param item: Dynamodb Item
    :type key: json (dictionary)
    :type item: json (dictionary)
    :returns: Dynamodb Response object
    :rtype: json (dictionary)
    """

    resp = self.DYNAMODB_c.update_item(
      TableName = self.tableName,
      Key = key,
      AttributeUpdates = item
    )
    return resp

  def increment(self, key, attribute):
    """
    Atomic Number increment
    :param key: Item Key
    :param attribute: Attrib to increment
    """

    resp = self.DYNAMODB_c.update_item(
      TableName = self.tableName,
      Key = key,
      UpdateExpression = 'ADD #'+attribute+' :inc',
      ExpressionAttributeValues = {
        ':inc' : {
          'N' : '1'
        }
      },
      ExpressionAttributeNames = {
        '#'+attribute : attribute
      },
      ReturnValues='UPDATED_NEW'
    )
    return resp

  def get_item(self, key):
    """
    Retrieve Dynamodb Record
    :param key: Item key
    :type key: json (dictionary)
    :returns: Dynamodb Response object
    :rtype: json (dicionary)
    """

    resp = self.DYNAMODB_c.get_item(
      TableName = self.tableName,
      Key = key
    )

    return resp

  def batch_delete(self, items):
    """
    Dynamodb batch delete items
    :param item: Dynamodb Items to be deleted
    :type item: json (dictionary)
    """

    table = self.DYNAMODB_r.Table(self.tableName)

    with table.batch_writer() as batch:
      for item in items:
        batch.delete_item(Key=item)

  def batch_put(self, items):
    """
    Dynamodb batch insert items
    :param item: Dynamodb Items to be inserted
    :type item: json (dictionary)
    """

    table = self.DYNAMODB_r.Table(self.tableName)
    
    with table.batch_writer() as batch:
      for item in items:
        batch.put_item(Item=item)

  def query(self, keyExpression):
    """
    Dynamodb query
    :param keyExpression: Dynamodb KeyConditionExpression
    :type keyExpression: Key (boto3.key)
    :returns: Dynamodb Response object
    :rtype: json (dicionary)
    """

    table = self.DYNAMODB_r.Table(self.tableName)

    resp = table.query(KeyConditionExpression=keyExpression)
    return resp['Items']    

  


 
