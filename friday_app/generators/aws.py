"""
Authored by Kim Clarence Penaflor
08/05/2019
version 0.0.01
Documented via reST

AWS Resource Generator
"""

import uuid
import boto3
from friday_app.shared.configuration import config

global S3
global DYNAMODB

_config = {
  'aws_id' : config.var('AWS_ACCESS_KEY_ID'),
  'aws_secret' : config.var('AWS_SECRET_ACCESS_KEY')
}

DYNAMODB = boto3.resource('dynamodb', _config)
S3 = boto3.client('s3', _config)


# TODO: Save Cloud Config
def _save_cloud_config():
  pass


# Initialize Dynamodb Table
# TODO: Initialize Dynamodb Table
def _init_table():
  global DYNAMODB
  pass




