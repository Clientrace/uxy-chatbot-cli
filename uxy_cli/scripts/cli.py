"""
Authored by Kim Clarence Penaflor
08/09//2019
version 0.0.2
Documented via reST

Project uxy cli command manager module
"""


import json
import boto3
import click
import uxy_cli
from uxy_cli._handlers import setup_handler
from uxy_cli._handlers import cleanup_handler
from uxy_cli._handlers import deployment_handler

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

  botoSession = boto3.session.Session()
  default_region = botoSession.region_name

  appDesc = click.prompt('Description ', type=str)
  stage = click.prompt('Stage ', type=str, default='dev', show_default='dev')
  region = click.prompt('Region ', type=str, default=default_region, show_default=default_region)
  setup_handler._setup_(appname, runtime, appDesc, stage, region)


@cli.command('purge')
def purge():
  """
  Removes project
  """

  if(click.confirm('Are you sure you want to remove the project and its resources?')):
    cleanup_handler.purge()


@cli.command('deploy')
def deploy():
  """
  Deploy chatbot project
  """
  pass



# TODO: Uxy Chatbot Component generator
def generate_component():
  pass


if __name__ == '__main__':
  cli()






