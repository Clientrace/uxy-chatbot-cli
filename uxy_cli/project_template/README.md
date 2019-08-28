# :appname:

This project was generated with uxy-chatbot-cli version 0.0.1

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


## Setup
Generate your facebook page token:
developers.facebook.com\
Products > Webhooks > Messenger > Settings > Access Tokens > Add page > Generate Token

Set your facebook page token
src/env/enviornment.dev.cfg
```
[FACEBOOK]
FB_PAGE_TOKEN = <your generated token>
```

## FB App Integration
developers.facebook.com/apps
```
uxy info
```
Capture the invocation URL and the verification token
```
FB Verify Token: abcdefghi1234567890123456789test
IAM ARN: arn:aws:iam::12345678:role/friday-uxy-app
Lambda ARN: arn:aws:lambda:ap-southeast-1:12345678:function:friday-uxy-app-dev
Invocation URL: https://sampleurl.execute-api.ap-southeast-1.amazonaws.com/v1/uxy-webhook
```

Enter the invocation URL and fb verify token in webhook setting\
Products > Webhooks > Messenger > Settings > Webhooks
```
Callback URL: https://sampleurl.execute-api.ap-southeast-1.amazonaws.com/v1/uxy-webhook
Verify Token: abcdefghi1234567890123456789test
```


## Deployment
```
uxy deploy
```
