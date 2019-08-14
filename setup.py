from setuptools import setup, find_packages

requirements = open('requirements.txt').read().split('\n')

setup(
  name = 'uxy',
  version = '0.0.2',
  packages = find_packages(),
  include_package_data=True,
  install_requires = requirements,
  entry_points = '''
  [console_scripts]
  uxy=uxy_cli.scripts.cli:cli
  '''
)




