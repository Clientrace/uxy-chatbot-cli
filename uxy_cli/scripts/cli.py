"""
Authored by Kim Clarence Penaflor
08/09//2019
version 0.0.4
Documented via reST

Project uxy cli command manager module
"""

import os
import json
import boto3
import click
import uxy_cli
from uxy_cli._handlers import setup_handler
from uxy_cli._handlers import cleanup_handler
from uxy_cli._handlers import deployment_handler
from uxy_cli._handlers import applogs_handler
from uxy_cli._handlers import info_handler

@click.group()
def cli():
  """ 
  \b
      __  ___  ____  __   ________    ____
     / / / / |/ /\ \/ /  / ____/ /   /  _/
    / / / /|   /  \  /  / /   / /    / /  
   / /_/ //   |   / /  / /___/ /____/ /   
   \____//_/|_|  /_/   \____/_____/___/   
  """

@cli.command('new')
@click.argument('appname')
@click.option('-r','--runtime', default='python', help='application runtime', type=click.Choice(['python','go']))
def new(appname, runtime):
  """
  Creates new project.
  """

  if( os.path.exists(appname)):
    print('Project: '+appname+' already exists..')
    print('Aborting..')
    return

  botoSession = boto3.session.Session()
  default_region = botoSession.region_name

  appDesc = click.prompt('Description ', type=str)
  stage = click.prompt('Stage ', type=str, default='dev', show_default='dev')
  region = click.prompt('Region ', type=str, default=default_region, show_default=default_region)
  setup_handler.setup(appname, runtime, appDesc, stage, region)


@cli.command('purge')
def purge():
  """
  Removes project
  """

  if(click.confirm('Are you sure you want to remove the project and its resources?')):
    cleanup_handler.purge()


@cli.command('info')
@click.option('-s','--stage')
def info(stage):
  """
  Get chatbot info
  """

  info_handler.get_cloud_blueprint(stage)


@cli.command('deploy')
@click.option('-s','--stage')
def deploy(stage):
  """
  Deploy chatbot project
  """
  deployment_handler.deploy(stage)

@cli.command('logs')
def logs():
  """
  Get application logs
  """
  applogs_handler.getlogs()



# TODO: Uxy Chatbot Component generator
def generate_component():
  pass


if __name__ == '__main__':
  # TODO: Detect if awscli is installed and configured
  cli()






