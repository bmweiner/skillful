# skillful

*A Python package for building Amazon Alexa skills.*

## Features

* Implements request and response objects compliant with the [JSON Interface
  Reference for Custom Skills](https://goo.gl/JpVGm4), version 1.0
* Function decorators for registering function logic to be performed when
  specific request types are received
* Automatic request processing which handles parsing, validation, dispatch,
  and response

## Installation

    pip install skillful

## Example

    import skillful
    from skillful.tests import data

    application_id = 'amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe'
    skill = skillful.Skill(application_id)

    @skill.launch
    def on_launch():
        print('Launched: {}'.format(skill.request.session.session_id))
        text = 'Welcome to skillful. Would you like to build an Alexa skill?'
        skill.response.set_output_speech_plain_text(text)
        ssml = ('<speak>Please tell me if you would like to build an Alexa '
                'skill.</speak>')
        skill.response.set_reprompt_output_speech_ssml(ssml)

    @skill.intent('yes')
    def on_intent_yes():
        text = ('Great! Building Alexa skills is easy with skillful. Open '
                'the Alexa app to see more information on skillful, a '
                'Python package for building Alexa skills.')
        skill.response.set_output_speech_plain_text(text)
        title = 'skillful'
        content = ('A Python package for building Alexa skills.\n\n'
                   'Visit: https://github.com/bmweiner/skillful')
        skill.response.set_card_type_simple(title, content)
        skill.terminate()

    @skill.intent('no')
    def on_intent_no():
        text = ('Well, if you change your mind, open the Alexa app to see '
                'more information on skillful, a Python package for '
                'building Alexa skills.')
        skill.response.set_output_speech_plain_text(text)
        title = 'skillful'
        content = ('A Python package for building Alexa skills.\n\n'
                   'Visit: https://github.com/bmweiner/skillful')
        skill.response.set_card_type_simple(title, content)
        skill.terminate()

    @skill.session_ended
    def on_session_ended():
        print('Ended: {}'.format(skill.request.session.session_id))
        skill.terminate()

    # simulate request body
    body = data.SAMPLE_LAUNCH_REQUEST
    skill.process(body)

Output:

    Launched: amzn1.echo-api.session.0000000-0000-0000-0000-00000000000

    {
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
    }
