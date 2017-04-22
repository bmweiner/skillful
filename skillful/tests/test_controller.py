"""skillful controller module tests"""
# pylint: disable=protected-access
# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import unittest
from skillful import controller
from skillful import interface
from skillful.tests import data


class TestSkill(unittest.TestCase):
    """Test Skill class."""
    @classmethod
    def setUpClass(cls):
        cls.skill = controller.Skill()

    def test___init__(self):
        """Test __init__ method."""
        self.assertIsNone(self.skill.application_id)
        self.assertIsInstance(self.skill.request, interface.RequestBody)
        self.assertIsInstance(self.skill.response, interface.ResponseBody)
        self.assertIsInstance(self.skill.logic, dict)
        self.assertTrue(callable(self.skill.launch))
        self.assertTrue(callable(self.skill.intent))
        self.assertTrue(callable(self.skill.session_ended))

    def test_register(self):
        """Test register method."""
        @self.skill.register('test_logic')
        def sample_func():
            """Decorated function."""
            return True
        self.assertTrue(self.skill.logic['test_logic']())

    def test_register_context_error(self):
        """Test register method for context error."""
        @self.skill.register('test_logic')
        def sample_func():
            """Decorated function."""
            pass
        self.skill.logic['test_logic']()
        self.assertRaises(RuntimeError, sample_func)

    def test_pass_attributes(self):
        """Test pass_attributes method."""
        self.skill.request.session.attributes = {'name': 'skill', 'age': 10}
        self.skill.pass_session_attributes()
        actual = self.skill.response.sessionAttributes
        self.assertEqual(actual['name'], 'skill')
        self.assertEqual(actual['age'], 10)

    def test_terminate(self):
        """Test terminate method."""
        self.skill.terminate()
        self.assertTrue(self.skill.response.response.shouldEndSession)

    def test_dispatch_launch(self):
        """Test dispath method for launch."""
        @self.skill.launch
        def sample_func():
            """Decorated function."""
            self.skill.response.sessionAttributes['run'] = True
        self.skill.request.request.type = 'LaunchRequest'
        self.skill.dispatch()
        self.assertTrue(self.skill.response.sessionAttributes['run'])

    def test_dispatch_intent(self):
        """Test dispath method for intent."""
        @self.skill.intent('test_intent')
        def sample_func():
            """Decorated function."""
            self.skill.response.sessionAttributes['run'] = True
        self.skill.request.request.type = 'IntentRequest'
        self.skill.request.request.intent = interface.Intent()
        self.skill.request.request.intent.name = 'test_intent'
        self.skill.dispatch()
        self.assertTrue(self.skill.response.sessionAttributes['run'])

    def test_dispatch_session_end(self):
        """Test dispath method for session_end."""
        @self.skill.session_ended
        def sample_func():
            """Decorated function."""
            self.skill.response.sessionAttributes['run'] = True
        self.skill.request.request.type = 'SessionEndedRequest'
        self.skill.dispatch()
        self.assertTrue(self.skill.response.sessionAttributes['run'])

    def test_dispatch_missing(self):
        """Test dispath method for missing."""
        self.skill.logic = {}
        self.assertRaises(KeyError, self.skill.dispatch)

    def test_valid_request_false(self):
        """Test valid_request method for false."""
        self.skill.application_id = '12345'
        self.assertFalse(self.skill.valid_request())

    def test_valid_request_true(self):
        """Test valid_request method for true."""
        self.skill.application_id = '12345'
        self.skill.request.session.application.application_id = '12345'
        self.assertTrue(self.skill.valid_request())

    def test_process(self):
        """Test process method."""
        self.skill.logic = {}
        @self.skill.launch
        def sample_func():
            """Decorated function."""
            self.skill.response.set_speech_text('Welcome to skillful.')
            self.skill.response.set_reprompt_ssml('<speak>Hello.</speak>')
        actual = self.skill.process(data.SAMPLE_LAUNCH_REQUEST)
        self.assertRegexpMatches(actual, '"version": "1.0"')
        self.assertRegexpMatches(actual, '"text": "Welcome to skillful."')
        self.assertRegexpMatches(actual, '"shouldEndSession": false')
        self.assertRegexpMatches(actual, '"ssml": "<speak>Hello.</speak>"')

    def test_process_invalid(self):
        """Test process method for invalid."""
        self.skill.logic = {}
        self.skill.application_id = '12345'
        @self.skill.launch
        def sample_func():
            """Decorated function."""
            pass
        self.skill.logic['LaunchRequest']()
        actual = self.skill.process(data.SAMPLE_LAUNCH_REQUEST)
        expected = """{"InternalServerError":"invalid application_id"}"""
        self.assertEqual(actual, expected)

    def test_process_end(self):
        """Test process method for invalid."""
        self.skill.logic = {}
        @self.skill.session_ended
        def sample_func():
            """Decorated function."""
            pass
        actual = self.skill.process(data.SAMPLE_SESSION_ENDED_REQUEST)
        expected = '"response": {"shouldEndSession": true}'
        self.assertRegexpMatches(actual, expected)
