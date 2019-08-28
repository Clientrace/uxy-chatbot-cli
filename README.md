uxy-chatbot-cli
======
This is an AWS chatbot framework for python and initially intended for personal use but then I decided
to share it here. This heavily rely on amazon for its infra and you'll need an AWS account to use this (it's not
that hard creating one: https://portal.aws.amazon.com/billing/signup#/start). Amazon also provides free
tier access for new users and this can also be (if you're not familiar with amazon yet)the start of your
journey in amazon web services. Uxy uses aws lambda for the application logic, aws dynamodb for state/conversation
data storing, s3 bucket for resource blueprint and assets storage, and api gateway for exposing a RESTful endpoint
that you need to integrate with your Facebook application. I'm also planning to add other messaging channel
like telegram, viber, twitter in the future. Have fun.

#### Project Package Structure
```
|── _uxy_core
| |── _components
| |── _modules
| |   |── e2e
| |   └── msg_platforms
| └── utility
|     |── api_wrappers
|     └── aws_services
└──src
  |── components
  |   |── unit
  |   └── view
  |── content
  |   |── assets
  |   └── spiels
  └── env
```

* **_uxy_core** - application core modules
* **src** - chatbot source files


#### Application Configuration (uxy.json)
```
{
 "app:name": <application name>,
 "app:version": <application version>,
 "app:description" : <application description>,
 "app:runtime" : <application language runtime>,
 "app:stage" : <application deverlopment stage>,
 "app:config" : {
  "dev" : {	<development environment>
   "fileReplacements" : [
    {
     "replace" : <file to replace>,
     "with" : <replacement file>
		}
   ]
 },
 "prod" : {	<production environment>
  "fileReplacements" : [
    {
     "replace" : <file to replace>,
     "with" : <replacement file>
    }
   ]
  }
 },
 "aws:config" : { <aws configuration>
 "region" : <aws region>,
 "dynamodb:session-table" : { <user-chatbot session table>
   "wcu" : <aws dynamodb write capacity unit (default is 5)>,
   "rcu" : <aws dynamodb read capacity unit (default is 5)>
  }
 }
}
```

