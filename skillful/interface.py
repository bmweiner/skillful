"""Implements request and response body objects."""

from __future__ import absolute_import, division, print_function
import json
import six

class DefaultAttrMixin(object):
    """Sets default attributes"""
    def _set_default_attr(self, default_attr):
        """Sets default attributes when None.

        Args:
            default_attr: dict. Key-val of attr, default-value.
        """
        for attr, val in six.iteritems(default_attr):
            if getattr(self, attr, None) is None:
                setattr(self, attr, val)

class Body(DefaultAttrMixin):
    """Base HTTP body class"""
    def __repr__(self):
        return ('<' + self.__class__.__name__ + ' ' +
                self.to_json(False, False) + '>')

    def __len__(self):
        return len(self.__dict__)

    def to_json(self, drop_null=True, camel=True, indent=None, sort_keys=False):
        """Serialize self as JSON

        Args:
            drop_null: bool, default True. Remove 'empty' attributes. See
                to_dict.
            camel: bool, default True. Convert keys to camelCase.
            indent: int, default None. See json built-in.
            sort_keys: bool, default False. See json built-in.

        Return:
            str: object params.
        """
        return json.dumps(self.to_dict(drop_null, camel), indent=indent,
                          sort_keys=sort_keys)

    def to_dict(self, drop_null=True, camel=True):
        """Serialize self as dict.

        Args:
            drop_null: bool, default True. Remove 'empty' attributes.
            camel: bool, default True. Convert keys to camelCase.

        Return:
            dict: object params.
        """
        return _to_dict(self, drop_null, camel)

class BodyChild(DefaultAttrMixin):
    """Base HTTP Body child class"""
    def __repr__(self):
        return '<' + self.__class__.__name__ + ' ' + str(self.__dict__) + '>'

    def __len__(self):
        return len(self.__dict__)

# implement request
class RequestBody(Body):
    """Implements the HTTP body for a custom request.

    Compliant with version 1.0 of the JSON Interface Reference for Custom
        Skills: https://goo.gl/JpVGm4.

    Attributes:
        version: str. Version specifier for the request.
        session: obj. Context associated with the session see Session class.
        request: obj. Context association with the user, see Request class.
    """
    def __init__(self, version=None, session=None, request=None):
        """Inits a RequestBody class with placeholder params."""
        default_attr = dict(version=str(),
                            session=Session(),
                            request=Request())
        self.version = version
        self.session = session
        self.request = request
        self._set_default_attr(default_attr)

    def parse(self, body):
        """Parse JSON request, storing content in object attributes.

        Args:
            body: dict. HTTP request body. If str is passed, parse will attempt
                conversion to dict.

        Returns:
            self
        """
        if isinstance(body, six.string_types):
            body = json.loads(body)

        # version
        version = body['version']
        self.version = version

        # session
        session = body['session']
        self.session.new = session['new']
        self.session.session_id = session['sessionId']
        application_id = session['application']['applicationId']
        self.session.application.application_id = application_id
        if 'attributes' in session and session['attributes']:
            self.session.attributes = session.get('attributes', {})
        else:
            self.session.attributes = {}
        self.session.user.user_id = session['user']['userId']
        self.session.user.access_token = session['user'].get('accessToken', 0)

        # request
        request = body['request']

        # launch request
        if request['type'] == 'LaunchRequest':
            self.request = LaunchRequest()

        # intent request
        elif request['type'] == 'IntentRequest':
            self.request = IntentRequest()
            self.request.intent = Intent()
            intent = request['intent']
            self.request.intent.name = intent['name']
            if 'slots' in intent and intent['slots']:
                for slot_name, slot in six.iteritems(intent['slots']):
                    self.request.intent.slots[slot_name] = Slot()
                    self.request.intent.slots[slot_name].name = slot['name']
                    self.request.intent.slots[slot_name].value = slot['value']

        # session ended request
        elif request['type'] == 'SessionEndedRequest':
            self.request = SessionEndRequest()
            self.request.reason = request['reason']

        # common - keep after specific requests to prevent param overwrite
        self.request.type = request['type']
        self.request.request_id = request['requestId']
        self.request.timestamp = request['timestamp']

        return self

class Session(BodyChild):
    """Request context associated with the session.

    Attributes
        new: bool. Indicates if session is new.
        session_id: str. Unique identifier for user's active session, consistent
            while the session is active.
        attributes: dict. Key-value pairs for attribute name-value. Empty for
            new requests.
        application: obj. Context associated with the application. See
            Application class.
        user: obj. Context associated with the user. See User class.
    """
    def __init__(self, new=None, session_id=None, attributes=None,
                 application=None, user=None):
        """Inits a Session class with placeholder params."""
        default_attr = dict(new=bool(),
                            session_id=str(),
                            attributes=dict(),
                            application=Application(),
                            user=User())
        self.new = new
        self.session_id = session_id
        self.attributes = attributes
        self.application = application
        self.user = user
        self._set_default_attr(default_attr)

class Application(BodyChild):
    """Request context association with the application.

    Attributes:
        application_id: str. Intended application id for request. Used when
            Skill class initialized with application_id for validation.
    """
    def __init__(self, application_id=None):
        """Inits an Application class with placeholder params."""
        default_attr = dict(application_id=None)
        self.application_id = application_id
        self._set_default_attr(default_attr)

class User(BodyChild):
    """Request context associated with the user.

    Arguments:
        user_id: str. Unique identifier for the user. Length can vary, but is
            always less than 255 characters. A user_id will change if a user
            disables then re-enables the skill.
        access_token: str. User token for a linked account, if configured.
    """
    def __init__(self, user_id=None, access_token=None):
        """Inits a User class with placeholder params."""
        default_attr = dict(user_id=str(),
                            access_token=str())
        self.user_id = user_id
        self.access_token = access_token
        self._set_default_attr(default_attr)

class Request(BodyChild):
    """Request context associated with all requests.

    Attributes:
        type: str. Type of request, possible values are: ['LaunchRequest',
            'IntentRequest', 'SessionEndedRequest'].
        request_id: str. Unique identifier for request.
        timestamp: str. ISO 8601 formatted time and date when request sent.
    """
    def __init__(self, type_=None, request_id=None, timestamp=None):
        """Inits a Request class with placeholder params."""
        default_attr = dict(type=str(),
                            request_id=str(),
                            timestamp=str())
        self.type = type_
        self.request_id = request_id
        self.timestamp = timestamp
        self._set_default_attr(default_attr)

class LaunchRequest(Request):
    """Request context associated with a launch request.

    See Request base class for additional info.
    """
    def __init__(self):
        """Inits a LaunchRequest class with placeholder params."""
        super(LaunchRequest, self).__init__()

class IntentRequest(Request):
    """Request context associated with an intent request.

    See Request base class for additional info.

    Arguments:
        intent: obj. Context associated with the intent.
    """
    def __init__(self, intent=None):
        """Inits an IntentRequest class with placeholder params."""
        super(IntentRequest, self).__init__()
        default_attr = dict(intent=Intent())
        self.intent = intent
        self._set_default_attr(default_attr)

class Intent(BodyChild):
    """Request context associated with an intent.

    Arguments:
        name: str. Name of the intent.
        slots: dict. Key-value pairs containing slot values per predefined
            schema.
    """
    def __init__(self, name=None, slots=None):
        """Inits an Intent class with placeholder params."""
        default_attr = dict(name=str(),
                            slots=dict())
        self.name = name
        self.slots = slots
        self._set_default_attr(default_attr)

class Slot(BodyChild):
    """Request context associated with an intent slot.

    Arguments:
        name: str. Name of slot.
        value: str. Value of the slot.
    """
    def __init__(self, name=None, value=None):
        """Inits a Slot class with placeholder params."""
        default_attr = dict(name=str(),
                            value=str())
        self.name = name
        self.value = value
        self._set_default_attr(default_attr)

class SessionEndRequest(Request):
    """Request context associated with a session ended request.

    See Request base class for additional info.

    Attributes:
        reason: str. Reason session ended, possible values are:
            ['USER_INITIATED', 'ERROR', 'EXCEEDED_MAX_REPROMPTS']
    """
    def __init__(self, reason=None):
        """Inits a SessionEndRequest class with placeholder params."""
        super(SessionEndRequest, self).__init__()
        default_attr = dict(reason=str())
        self.reason = reason
        self._set_default_attr(default_attr)

# implement response
class ResponseBody(Body):
    """Implements the HTTP body for a custom response.

    Compliant with version 1.0 of the JSON Interface Reference for Custom
        Skills: https://goo.gl/JpVGm4.

    Total response size cannot exceed 24 kilobytes.

    Attributes:
        version: str, default '1.0'. Version specifier for the response.
        session_attributes: dict. Key-value pairs for attribute name-value.
        response: obj. Context association with the response, see Response
            class.
    """
    def __init__(self, version=None, session_attributes=None, response=None):
        """Inits a ResponseBody class with placeholder params."""
        default_attr = dict(version='1.0',
                            session_attributes=dict(),
                            response=Response())
        self.version = version
        self.session_attributes = session_attributes
        self.response = response
        self._set_default_attr(default_attr)

    def set_session_attribute(self, key, value):
        """Store session attribute.

        Args:
            key: str. Attribute name.
            value: object. Attribute value.
        """
        self.session_attributes[key] = value

    def get_session_attribute(self, key):
        """Get session attribute.

        Args:
            key: str. Attribute name.

        Returns:
            value: object.
        """
        return self.session_attributes.get(key, None)

    def set_output_speech_plain_text(self, text):
        """Set response output speech as plain text type.

        Args:
            text: str. Response speech used when type is 'PlainText'. Cannot exceed
                8,000 characters.
        """
        self.response.output_speech.type = 'PlainText'
        self.response.output_speech.text = text

    def set_output_speech_ssml(self, ssml):
        """Set response output speech as SSML type.

        Args:
            ssml: str. Response speech used when type is 'SSML', should be formatted
                with Speech Synthesis Markup Language. Cannot exceed 8,000
                characters.
        """
        self.response.output_speech.type = 'SSML'
        self.response.output_speech.ssml = ssml

    def set_card_type_simple(self, title, content):
        """Set response card as simple type.

        title and content cannot exceed 8,000 characters.

        Args:
            title: str. Title of Simple or Standard type card.
            content: str. Content of Simple type card.
        """
        self.response.card.type = 'Simple'
        self.response.card.title = title
        self.response.card.content = content

    def set_card_type_standard(self, title, text, small_image_url=None,
                               large_image_url=None):
        """Set response card as standard type.

        title, text, and image cannot exceed 8,000 characters.

        Args:
            title: str. Title of Simple or Standard type card.
            text: str. Content of Standard type card.
            small_image_url: str. URL of small image. Cannot exceed 2,000
                characters. Recommended pixel size: 720w x 480h.
            large_image_url: str. URL of large image. Cannot exceed 2,000
                characters. Recommended pixel size: 1200w x 800h.
        """
        self.response.card.type = 'Standard'
        self.response.card.title = title
        self.response.card.text = text
        if not small_image_url and large_image_url:
            delattr(self.response.card, 'image')
        if small_image_url:
            self.response.card.image.small_image_url = small_image_url
        if large_image_url:
            self.response.card.image.large_image_url = large_image_url

    def set_card_type_link_account(self):
        """Set response card as link account type."""
        self.response.card.type = 'LinkAccount'

    def set_reprompt_output_speech_plain_text(self, text):
        """Set response reprompt output speech as plain text type.

        Args:
            text: str. Response speech used when type is 'PlainText'. Cannot
                exceed 8,000 characters.
        """
        self.response.reprompt.output_speech.type = 'PlainText'
        self.response.reprompt.output_speech.text = text

    def set_reprompt_output_speech_ssml(self, ssml):
        """Set response reprompt output speech as SSML type.

        Args:
            ssml: str. Response speech used when type is 'SSML', should be formatted
                with Speech Synthesis Markup Language. Cannot exceed 8,000
                characters.
        """
        self.response.reprompt.output_speech.type = 'SSML'
        self.response.reprompt.output_speech.ssml = ssml

    def set_should_end_session(self, end):
        """Set response should end session

        Args:
            should_end_session: bool. If True, end the session.
        """
        self.response.should_end_session = end

class Response(BodyChild):
    """Response context associated with all responses.

    Attributes:
        output_speech: obj. Context associated with the output speech.
        card: obj. Context associated with the card.
        reprompt: obj. Context associated with a reprompt.
        should_end_session: bool. If True, end the session.
    """
    def __init__(self, output_speech=None, card=None, reprompt=None,
                 should_end_session=None):
        """Inits a Response class with placeholder params."""
        default_attr = dict(output_speech=OutputSpeech(),
                            card=Card(),
                            reprompt=Reprompt(),
                            should_end_session=False)
        self.output_speech = output_speech
        self.card = card
        self.reprompt = reprompt
        self.should_end_session = should_end_session
        self._set_default_attr(default_attr)

class OutputSpeech(BodyChild):
    """Response context associated with output speech.

    Attributes:
        type: str. Type of speech, possible values are ['PlainText', 'SSML'].
        text: str. Response speech used when type is 'PlainText'. Cannot exceed
            8,000 characters.
        ssml: str. Response speech used when type is 'SSML', should be formatted
            with Speech Synthesis Markup Language. Cannot exceed 8,000
            characters.
        """
    def __init__(self, type_=None, text=None, ssml=None):
        """Inits a OutputSpeech class with placeholder params."""
        default_attr = dict(type=str(),
                            text=str(),
                            ssml=str())
        self.type = type_
        self.text = text
        self.ssml = ssml
        self._set_default_attr(default_attr)

class Card(BodyChild):
    """Response context associated with card to render.

    title, content, text, and image cannot exceed 8,000 characters.

    Attributes:
        type: str. Type of card, possible values are ['Simple', 'Standard',
            'LinkAccount']
        title: str. Title of Simple or Standard type card.
        content: str. Content of Simple type card.
        text: str. Content of Standard type card.
        image: str. Context associated with a card image.
    """
    def __init__(self, type_=None, title=None, content=None, text=None,
                 image=None):
        """Inits a Card class with placeholder params."""
        default_attr = dict(type=str(),
                            title=str(),
                            content=str(),
                            text=str(),
                            image=Image())
        self.type = type_
        self.title = title
        self.content = content
        self.text = text
        self.image = image
        self._set_default_attr(default_attr)

class Image(BodyChild):
    """Response context associated with a card image.

    Attributes:
        small_image_url: str. URL of small image. Cannot exceed 2,000
            characters. Recommended pixel size: 720w x 480h.
        large_image_url: str. URL of large image. Cannot exceed 2,000
            characters. Recommended pixel size: 1200w x 800h.
    """
    def __init__(self, small_image_url=None, large_image_url=None):
        """Inits an Image class with placeholder params."""
        default_attr = dict(small_image_url=str(),
                            large_image_url=str())
        self.small_image_url = small_image_url
        self.large_image_url = large_image_url
        self._set_default_attr(default_attr)

class Reprompt(BodyChild):
    """Response context associated with a reprompt.

    Attributes:
        output_speech: obj. Context associated with the output speech.
    """
    def __init__(self, output_speech=None):
        """Inits a Reprompt class with placeholder params."""
        default_attr = dict(output_speech=OutputSpeech())
        self.output_speech = output_speech
        self._set_default_attr(default_attr)

def _to_dict(obj, drop_null=True, camel=True):
    """Serialize obj as dict.

    Args:
        obj: obj. Object to serialize.
        drop_null: bool, default True. Remove 'empty' attributes.
        camel: bool, default True. Convert keys to camelCase.

    Return:
        dict: obj serialized as dict.
    """
    if isinstance(obj, (Body, BodyChild)):
        obj = obj.__dict__
    if isinstance(obj, dict):
        data = {}
        for attr, val in six.iteritems(obj):
            if drop_null:
                cond = (isinstance(val, bool) or val == 0
                        or (val and _to_dict(val, drop_null, camel)))
            else:
                cond = True
            if cond:
                if camel:
                    attr = _snake_to_camel(attr)
                data[attr] = _to_dict(val, drop_null, camel)
        return data
    elif isinstance(obj, list):
        data = []
        for val in obj:
            if drop_null:
                cond = (isinstance(val, bool) or val == 0
                        or (val and _to_dict(val, drop_null, camel)))
            else:
                cond = True
            if cond:
                data.append(_to_dict(val, drop_null, camel))
        return data
    else:
        return obj

def _snake_to_camel(name, strict=False):
    """Converts parameter names from snake_case to camelCase.

    Args:
        name, str. Snake case.
        strict: bool, default True. If True, will set name to lowercase before
            converting, otherwise assumes original name is proper camel case.
            Set to False if name may already be in camelCase.

    Returns:
        str: CamelCase.
    """
    if strict:
        name = name.lower()
    terms = name.split('_')
    return terms[0] + ''.join([term.capitalize() for term in terms[1:]])
