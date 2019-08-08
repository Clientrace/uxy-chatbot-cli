from uxy_cli.generators.aws_setup import AWSSetup

appConfig = {
  'app:name' : 'testbot',
  'app:version' : 1,
  'description' : 'test chatbot',
  'runtime' : 'python3.6',
  'stage' : 'dev',
  'aws:configs' : {
    'dynamodb:session-table' : {
      'wcu' : 5,
      'rcu' : 5
    },
    'dynamodb:auth-table' : {
      'wcu' : 5,
      'rcu' : 5
    },
    'lambda:handler' : 'index.lambda_handler',
    'labmda:timeout' : 900
  },
  'verbosity' : True
}

awsSetup = AWSSetup(appConfig)
test = awsSetup.setup_iamRole()
print(test)


