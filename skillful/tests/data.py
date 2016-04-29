"""Sample JSON bodies for testing skills."""

SAMPLE_LAUNCH_REQUEST = """{
  "version": "1.0",
  "session": {
    "new": true,
    "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.account.AM3B00000000000000000000000"
    }
  },
  "request": {
    "type": "LaunchRequest",
    "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
    "timestamp": "2015-05-13T12:34:56Z"
  }
}"""

SAMPLE_INTENT_REQUEST = """{
  "version": "1.0",
  "session": {
    "new": false,
    "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
    },
    "attributes": {
      "profile": {
        "name": "skillful",
        "language": "Python",
        "awesome": true
      }
    },
    "user": {
      "userId": "amzn1.account.AM3B00000000000000000000000"
    }
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
    "timestamp": "2015-05-13T12:34:56Z",
    "intent": {
      "name": "yes",
      "slots": {
        "excitement": {
          "name": "level",
          "value": 10
        }
      }
    }
  }
}"""

SAMPLE_SESSION_ENDED_REQUEST = """{
  "version": "1.0",
  "session": {
    "new": false,
    "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
    },
    "attributes": {
      "profile": {
        "name": "skillful",
        "language": "Python",
        "awesome": true
      }
    },
    "user": {
      "userId": "amzn1.account.AM3B00000000000000000000000"
    }
  },
  "request": {
    "type": "SessionEndedRequest",
    "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
    "timestamp": "2015-05-13T12:34:56Z",
    "reason": "USER_INITIATED"
  }
}"""


SAMPLE_RESPONSE = """{
  "version": "1.0",
  "response": {
    "outputSpeech": {
      "text": "Welcome to skillful. Would you like to build an Alexa skill?",
      "type": "PlainText"
    },
    "shouldEndSession": false,
    "reprompt": {
      "outputSpeech": {
        "ssml": "<speak>Please tell me if you would like to build an Alexa skill.</speak>",
        "type": "SSML"
      }
    }
  }
}"""
