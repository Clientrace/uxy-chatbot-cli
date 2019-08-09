"""
Authored by Kim Clarence Penaflor
08/09//2019
version 0.0.2
Documented via reST

Project uxy cli command manager module
"""


import json
import click
from _handlers import setup_handler

global appinfo
appinfo = json.loads(open('cli.json').read())

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
@click.option('-r','--runtime', default='python', help='application runtime')
def new(appname, runtime):
  """
  Creates new project.
  """

  appDesc = click.prompt('Enter Description: ', type=str)
  setup_handler.__setup_aws_resources(appname, runtime, appDesc)


# TODO: Uxy Chatbot Component generator
def generate_component():
  pass




if __name__ == '__main__':
  cli()







