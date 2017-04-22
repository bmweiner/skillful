"""skillful interface module tests"""
# pylint: disable=protected-access
# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import unittest
from skillful import interface
from skillful.tests import data


class TestDefaultAttrMixin(unittest.TestCase):
    """Test DefaultAttrMixin class."""
    @classmethod
    def setUpClass(cls):
        class TestClass(interface.DefaultAttrMixin):
            """Test class inheriting DefaultAttrMixin."""
            def __init__(self, param_a, param_b=None, param_c=None):
                self.param_b = param_b
                self.param_c = param_c
        cls.test_class = TestClass((1, 2, 3), param_b='b')

    def test__set_default_attr(self):
        """Test _set_default_attr method."""
        default_attr = dict(param_b=1, param_c=['c'])
        self.test_class._set_default_attr(default_attr)
        self.assertEqual(self.test_class.param_b, 'b')
        self.assertEqual(self.test_class.param_c, ['c'])

class TestBody(unittest.TestCase):
    """Test Body class."""
    @classmethod
    def setUpClass(cls):
        cls.body = interface.Body()
        cls.body.param_a = 'a'
        cls.body.param_b = [1, '', {'a':None}]

    def test___repr__(self):
        """Test __repr__ method."""
        actual = str(self.body)
        self.assertEqual(actual[:8], '<Body {"')
        self.assertRegexpMatches(actual, '"param_a": "a"')
        self.assertRegexpMatches(actual, r'"param_b": \[1, "", \{"a": null\}\]')

    def test___len__(self):
        """Test __len__ method."""
        self.assertEqual(len(self.body), 2)

    def test_to_json(self):
        """Test to_json method."""
        expected = '{"paramA": "a", "paramB": [1]}'
        self.assertEqual(self.body.to_json(True, True, None, True), expected)

    def test_to_dict(self):
        """Test to_dict method."""
        actual = self.body.to_dict(True, True)
        self.assertEqual(actual['paramA'], 'a')
        self.assertEqual(len(actual['paramB']), 1)

    def test_to_dict_no_drop(self):
        """Test to_dict method for no drop."""
        actual = self.body.to_dict(False, True)
        self.assertEqual(actual['paramA'], 'a')
        self.assertEqual(len(actual['paramB']), 3)
        self.assertIsNone(actual['paramB'][2]['a'])

    def test_to_dict_no_camel(self):
        """Test to_dict method for no camel."""
        actual = self.body.to_dict(True, False)
        self.assertEqual(actual['param_a'], 'a')
        self.assertEqual(actual['param_b'], [1])

    def test_to_dict_no_drop_camel(self):
        """Test to_dict method for no drop or camel."""
        actual = self.body.to_dict(False, False)
        self.assertEqual(actual['param_a'], 'a')
        self.assertEqual(len(actual['param_b']), 3)
        self.assertIsNone(actual['param_b'][2]['a'])

class TestBodyChild(unittest.TestCase):
    """Test Body class."""
    @classmethod
    def setUpClass(cls):
        cls.bodyChild = interface.BodyChild()
        cls.bodyChild.param_a = 'a'
        cls.bodyChild.param_b = []

    def test___repr__(self):
        """Test __repr__ method."""
        actual = str(self.bodyChild)
        self.assertEqual(actual[:13], "<BodyChild {'")
        self.assertRegexpMatches(actual, "'param_a': 'a'")
        self.assertRegexpMatches(actual, r"'param_b': \[\]")

    def test___len__(self):
        """Test __len__ method."""
        self.assertEqual(len(self.bodyChild), 2)

class TestRequestBody(unittest.TestCase):
    """Test RequestBody class."""
    @classmethod
    def setUpClass(cls):
        cls.request_body = interface.RequestBody()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.request_body.version, str)
        self.assertIsInstance(self.request_body.session, interface.Session)
        self.assertIsInstance(self.request_body.request, interface.Request)

    def test_parse_launch_request(self):
        """Test parse method for launch request."""
        self.request_body.parse(data.SAMPLE_LAUNCH_REQUEST)
        self.assertEqual(self.request_body.version, '1.0')
        self.assertEqual(self.request_body.session.new, True)
        expected = 'amzn1.echo-api.session.0000000-0000-0000-0000-00000000000'
        self.assertEqual(self.request_body.session.session_id, expected)
        actual = self.request_body.session.application.application_id
        expected = 'amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe'
        self.assertEqual(actual, expected)
        self.assertEqual(self.request_body.session.attributes, {})
        expected = 'amzn1.account.AM3B00000000000000000000000'
        self.assertEqual(self.request_body.session.user.user_id, expected)
        self.assertEqual(self.request_body.request.type, 'LaunchRequest')
        expected = "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000"
        self.assertEqual(self.request_body.request.request_id, expected)
        expected = '2015-05-13T12:34:56Z'
        self.assertEqual(self.request_body.request.timestamp, expected)

    def test_parse_intent_request(self):
        """Test parse method for intent request."""
        self.request_body.parse(data.SAMPLE_INTENT_REQUEST)
        self.assertEqual(self.request_body.version, '1.0')
        self.assertEqual(self.request_body.session.new, False)
        expected = 'amzn1.echo-api.session.0000000-0000-0000-0000-00000000000'
        self.assertEqual(self.request_body.session.session_id, expected)
        actual = self.request_body.session.application.application_id
        expected = 'amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe'
        self.assertEqual(actual, expected)
        actual = self.request_body.session.attributes['profile']['name']
        self.assertEqual(actual, 'skillful')
        actual = self.request_body.session.attributes['profile']['language']
        self.assertEqual(actual, 'Python')
        actual = self.request_body.session.attributes['profile']['awesome']
        self.assertEqual(actual, True)
        expected = 'amzn1.account.AM3B00000000000000000000000'
        self.assertEqual(self.request_body.session.user.user_id, expected)
        self.assertEqual(self.request_body.request.type, 'IntentRequest')
        expected = "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000"
        self.assertEqual(self.request_body.request.request_id, expected)
        expected = '2015-05-13T12:34:56Z'
        self.assertEqual(self.request_body.request.timestamp, expected)
        self.assertEqual(self.request_body.request.intent.name, 'yes')
        actual = self.request_body.request.intent.slots['excitement'].name
        self.assertEqual(actual, 'level')
        actual = self.request_body.request.intent.slots['excitement'].value
        self.assertEqual(actual, 10)

    def test_parse_session_ended_request(self):
        """Test parse method for session ended request."""
        self.request_body.parse(data.SAMPLE_SESSION_ENDED_REQUEST)
        self.assertEqual(self.request_body.version, '1.0')
        self.assertEqual(self.request_body.session.new, False)
        expected = 'amzn1.echo-api.session.0000000-0000-0000-0000-00000000000'
        self.assertEqual(self.request_body.session.session_id, expected)
        actual = self.request_body.session.application.application_id
        expected = 'amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe'
        self.assertEqual(actual, expected)
        actual = self.request_body.session.attributes['profile']['name']
        self.assertEqual(actual, 'skillful')
        actual = self.request_body.session.attributes['profile']['language']
        self.assertEqual(actual, 'Python')
        actual = self.request_body.session.attributes['profile']['awesome']
        self.assertEqual(actual, True)
        expected = 'amzn1.account.AM3B00000000000000000000000'
        self.assertEqual(self.request_body.session.user.user_id, expected)
        self.assertEqual(self.request_body.request.type, 'SessionEndedRequest')
        expected = "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000"
        self.assertEqual(self.request_body.request.request_id, expected)
        expected = '2015-05-13T12:34:56Z'
        self.assertEqual(self.request_body.request.timestamp, expected)
        self.assertEqual(self.request_body.request.reason, 'USER_INITIATED')

class TestSession(unittest.TestCase):
    """Test Session class."""
    @classmethod
    def setUpClass(cls):
        cls.session = interface.Session()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.session.new, bool)
        self.assertIsInstance(self.session.session_id, str)
        self.assertIsInstance(self.session.attributes, dict)
        self.assertIsInstance(self.session.application, interface.Application)
        self.assertIsInstance(self.session.user, interface.User)

class TestApplication(unittest.TestCase):
    """Test Application class."""
    @classmethod
    def setUpClass(cls):
        cls.application = interface.Application()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsNone(self.application.application_id)

class TestUser(unittest.TestCase):
    """Test User class."""
    @classmethod
    def setUpClass(cls):
        cls.user = interface.User()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.user.user_id, str)
        self.assertIsInstance(self.user.access_token, str)

class TestRequest(unittest.TestCase):
    """Test Request class."""
    @classmethod
    def setUpClass(cls):
        cls.request = interface.Request()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.request.type, str)
        self.assertIsInstance(self.request.request_id, str)
        self.assertIsInstance(self.request.timestamp, str)

class TestLaunchRequest(unittest.TestCase):
    """Test LaunchRequest class."""
    @classmethod
    def setUpClass(cls):
        cls.launch_request = interface.LaunchRequest()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.launch_request.type, str)
        self.assertIsInstance(self.launch_request.request_id, str)
        self.assertIsInstance(self.launch_request.timestamp, str)

class TestIntentRequest(unittest.TestCase):
    """Test IntentRequest class."""
    @classmethod
    def setUpClass(cls):
        cls.intent_request = interface.IntentRequest()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.intent_request.type, str)
        self.assertIsInstance(self.intent_request.request_id, str)
        self.assertIsInstance(self.intent_request.timestamp, str)
        self.assertIsInstance(self.intent_request.intent, interface.Intent)

class TestIntent(unittest.TestCase):
    """Test Intent class."""
    @classmethod
    def setUpClass(cls):
        cls.intent = interface.Intent()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.intent.name, str)
        self.assertIsInstance(self.intent.slots, dict)

class TestSlot(unittest.TestCase):
    """Test Slot class."""
    @classmethod
    def setUpClass(cls):
        cls.slot = interface.Slot()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.slot.name, str)
        self.assertIsInstance(self.slot.value, str)

class TestSessionEndedRequest(unittest.TestCase):
    """Test SessionEndedRequest class."""
    @classmethod
    def setUpClass(cls):
        cls.session_ended_request = interface.SessionEndedRequest()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.session_ended_request.type, str)
        self.assertIsInstance(self.session_ended_request.request_id, str)
        self.assertIsInstance(self.session_ended_request.timestamp, str)
        self.assertIsInstance(self.session_ended_request.reason, str)

class TestResponseBody(unittest.TestCase):
    """Test ResponseBody class."""
    @classmethod
    def setUpClass(cls):
        cls.response_body = interface.ResponseBody()

    def test___init__(self):
        """Test __init__ method."""
        self.assertEqual(self.response_body.version, '1.0')
        self.assertIsInstance(self.response_body.sessionAttributes, dict)
        self.assertIsInstance(self.response_body.response, interface.Response)

    def test_set_session_attribute(self):
        """Test set_session_attribute method."""
        val = ['1', '2', '3']
        self.response_body.set_session_attribute('my_list', val)
        actual = self.response_body.sessionAttributes['my_list']
        self.assertEqual(actual, val)

    def test_get_session_attribute(self):
        """Test get_session_attribute method."""
        val = (True, False)
        self.response_body.sessionAttributes['my_tuple'] = val
        actual = self.response_body.get_session_attribute('my_tuple')
        self.assertEqual(actual, val)

    def test_set_speech_text(self):
        """Test set_speech_text method."""
        text = ('Alexa say this.')
        self.response_body.set_speech_text(text)
        actual = self.response_body.response.outputSpeech.type
        self.assertEqual(actual, 'PlainText')
        self.assertEqual(self.response_body.response.outputSpeech.text, text)

    def test_set_speech_ssml(self):
        """Test set_speech_ssml method."""
        ssml = ('<speak>Alexa say that.</speak>')
        self.response_body.set_speech_ssml(ssml)
        self.assertEqual(self.response_body.response.outputSpeech.type, 'SSML')
        self.assertEqual(self.response_body.response.outputSpeech.ssml, ssml)

    def test_set_card_simple(self):
        """Test set_card_simple method."""
        title = 'Simple card title.'
        content = 'Simple card content'
        self.response_body.set_card_simple(title, content)
        self.assertEqual(self.response_body.response.card.type, 'Simple')
        self.assertEqual(self.response_body.response.card.title, title)
        self.assertEqual(self.response_body.response.card.content, content)

    def test_set_card_standard(self):
        """Test set_card_standard method."""
        title = 'Standard card title.'
        text = 'Standard card text'
        self.response_body.set_card_standard(title, text)
        self.assertEqual(self.response_body.response.card.type, 'Standard')
        self.assertEqual(self.response_body.response.card.title, title)
        self.assertEqual(self.response_body.response.card.text, text)

    def test_set_card_standard_simg(self):
        """Test set_card_standard method for small image."""
        title = 'Standard card title.'
        text = 'Standard card text'
        smallImageUrl = 'https://github.com/bmweiner/skillful/simg.png'
        self.response_body.set_card_standard(title, text, smallImageUrl)
        self.assertEqual(self.response_body.response.card.type, 'Standard')
        self.assertEqual(self.response_body.response.card.title, title)
        self.assertEqual(self.response_body.response.card.text, text)
        actual = self.response_body.response.card.image.smallImageUrl
        self.assertEqual(actual, smallImageUrl)

    def test_set_card_standard_limg(self):
        """Test set_card_standard method for large image."""
        title = 'Standard card title.'
        text = 'Standard card text'
        largeImageUrl = 'https://github.com/bmweiner/skillful/limg.png'
        self.response_body.set_card_standard(title, text, None, largeImageUrl)
        self.assertEqual(self.response_body.response.card.type, 'Standard')
        self.assertEqual(self.response_body.response.card.title, title)
        self.assertEqual(self.response_body.response.card.text, text)
        actual = self.response_body.response.card.image.largeImageUrl
        self.assertEqual(actual, largeImageUrl)

    def test_set_card_standard_img(self):
        """Test set_card_standard method for both images."""
        title = 'Standard card title.'
        text = 'Standard card text'
        smallImageUrl = 'https://github.com/bmweiner/skillful/simg.png'
        largeImageUrl = 'https://github.com/bmweiner/skillful/limg.png'
        self.response_body.set_card_standard(title, text, smallImageUrl,
                                             largeImageUrl)
        self.assertEqual(self.response_body.response.card.type, 'Standard')
        self.assertEqual(self.response_body.response.card.title, title)
        self.assertEqual(self.response_body.response.card.text, text)
        actual = self.response_body.response.card.image.smallImageUrl
        self.assertEqual(actual, smallImageUrl)
        actual = self.response_body.response.card.image.largeImageUrl
        self.assertEqual(actual, largeImageUrl)

    def test_set_card_link(self):
        """Test set_card_link method."""
        self.response_body.set_card_link()
        self.assertEqual(self.response_body.response.card.type, 'LinkAccount')

    def test_set_reprompt_text(self):
        """Test set_reprompt_text method."""
        text = ('Alexa say this.')
        self.response_body.set_reprompt_text(text)
        actual = self.response_body.response.reprompt.outputSpeech.type
        self.assertEqual(actual, 'PlainText')
        actual = self.response_body.response.reprompt.outputSpeech.text
        self.assertEqual(actual, text)

    def test_set_reprompt_ssml(self):
        """Test set_reprompt_ssml method."""
        ssml = ('<speak>Alexa say that.</speak>')
        self.response_body.set_reprompt_ssml(ssml)
        actual = self.response_body.response.reprompt.outputSpeech.type
        self.assertEqual(actual, 'SSML')
        actual = self.response_body.response.reprompt.outputSpeech.ssml
        self.assertEqual(actual, ssml)

    def test_end_session_true(self):
        """Test end_session method for true."""
        self.response_body.set_end_session(True)
        self.assertTrue(self.response_body.response.shouldEndSession)

    def test_end_session_false(self):
        """Test end_session method for false."""
        self.response_body.set_end_session(False)
        self.assertFalse(self.response_body.response.shouldEndSession)

class TestResponse(unittest.TestCase):
    """Test Response class."""
    @classmethod
    def setUpClass(cls):
        cls.response = interface.Response()

    def test___init__(self):
        """Test __init__ method."""
        actual = self.response.outputSpeech
        self.assertIsInstance(actual, interface.OutputSpeech)
        self.assertIsInstance(self.response.card, interface.Card)
        self.assertIsInstance(self.response.reprompt, interface.Reprompt)
        self.assertFalse(self.response.shouldEndSession)

class TestOutputSpeech(unittest.TestCase):
    """Test OutputSpeech class."""
    @classmethod
    def setUpClass(cls):
        cls.outputSpeech = interface.OutputSpeech()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.outputSpeech.type, str)
        self.assertIsInstance(self.outputSpeech.text, str)
        self.assertIsInstance(self.outputSpeech.ssml, str)

class TestCard(unittest.TestCase):
    """Test Card class."""
    @classmethod
    def setUpClass(cls):
        cls.card = interface.Card()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.card.type, str)
        self.assertIsInstance(self.card.title, str)
        self.assertIsInstance(self.card.content, str)
        self.assertIsInstance(self.card.text, str)
        self.assertIsInstance(self.card.image, interface.Image)

class TestImage(unittest.TestCase):
    """Test Image class."""
    @classmethod
    def setUpClass(cls):
        cls.image = interface.Image()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsInstance(self.image.smallImageUrl, str)
        self.assertIsInstance(self.image.largeImageUrl, str)

class TestReprompt(unittest.TestCase):
    """Test Reprompt class."""
    @classmethod
    def setUpClass(cls):
        cls.reprompt = interface.Reprompt()

    def test___init__(self):
        """Test __init__ method."""
        actual = self.reprompt.outputSpeech
        self.assertIsInstance(actual, interface.OutputSpeech)

class TestErrorResponse(unittest.TestCase):
    """Test error_response method."""
    def test_error_response(self):
        """Test error_response method."""
        expected = """{"InternalServerError":"Unknown"}"""
        self.assertEqual(interface.error_response(), expected)

    def test_error_response_custom(self):
        """Test error_response method for custom message."""
        expected = """{"InternalServerError":"custom message"}"""
        self.assertEqual(interface.error_response('custom message'), expected)

class TestSnakeToCamel(unittest.TestCase):
    """Test _snake_to_camel method."""
    def test__snake_to_camel_single(self):
        """Test _snake_to_camel method for single."""
        self.assertEqual(interface._snake_to_camel('sInGle'), 'sInGle')

    def test__snake_to_camel_strict(self):
        """Test _snake_to_camel method for strict."""
        self.assertEqual(interface._snake_to_camel('sInGle', True), 'single')

    def test__snake_to_camel_long(self):
        """Test _snake_to_camel method for long."""
        self.assertEqual(interface._snake_to_camel('a_long_var'), 'aLongVar')
