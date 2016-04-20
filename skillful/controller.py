"""Handler for request processing"""

from __future__ import absolute_import, division, print_function
from functools import wraps
import six

from .interface import RequestBody
from .interface import ResponseBody


class Skill(object):
    """Class for parsing, validation, logic registering, and dispatch.

    References:
        - JSON Interface Reference for Custom Skills: https://goo.gl/JpVGm4.
        - Providing Home Cards for the Amazon Alexa App: https://goo.gl/mX9P5o.
        - Speech Synthesis Markup Language (SSML) Reference: https://goo.gl/2BHQjz.

    Attributes:
        application_id: str. Skill application ID.
        request: skillful.Request. Proxy for HTTP request body.
        response: skillful.Response. HTTP response body.
        logic: dict. Containes function logic for processing requests,
            key-value corresponds to name-func.
        launch: obj. Decorator for registering the launch request function.
            See register() for additional info.
        intent: obj. Decorator for registering a named intent request
            function. See register() for additional info.
        session_ended: obj. Decorator for registering the session ended
            request function. See register() for additional info.
    """
    def __init__(self, application_id=None):
        """Inits a Skill class with proxy request and response.

        Args:
            application_id: str, default None. Skill application ID, if set,
                will attempt to validate during process method.
        """
        self.application_id = application_id
        self.request = RequestBody()
        self.response = ResponseBody()
        self.logic = dict()
        self.launch = self.register('LaunchRequest')
        self.intent = self.register
        self.session_ended = self.register('SessionEndedRequest')

    def register(self, name):
        """Decorator for registering a named function in the sesion logic.

        Args:
            name: str. Function name.
            func: obj. Parameterless function to register.

        The following named functions must be registered:
            'LaunchRequest' - logic for launch request.
            'SessionEndedRequest': logic for session ended request.

        In addition, all intents must be registered by their names specified
            in the intent schema.

        The aliased decorators: @launch, @intent(name), and @session_ended exist
            as a convenience for registering specific functions.
        """
        def decorator(func):
            """Inner decorator, not used directly.

            Args:
                func: obj. Parameterless function to register.

            Returns:
                func: decorated function.
            """
            self.logic[name] = func
            @wraps(func)
            def wrapper():
                """Wrapper, not used directly."""
                raise RuntimeError('working outside of request context')
            return wrapper
        return decorator

    def set_attribute(self, key, value):
        """Convenience function to call response.set_session_attribute."""
        self.response.set_session_attribute(key, value)

    def get_attribute(self, key):
        """Convenience function to call response.get_session_attribute."""
        return self.response.get_session_attribute(key)

    def pass_attributes(self):
        """Copies request attributes to response"""
        for key, value in six.iteritems(self.request.session.attributes):
            self.response.session_attributes[key] = value

    def terminate(self):
        """Convenience function to call response.set_should_end_session True."""
        self.response.set_should_end_session(True)

    def dispatch(self):
        """Calls the matching logic function by request type or intent name."""

        if self.request.request.type == 'IntentRequest':
            name = self.request.request.intent.name
        else:
            name = self.request.request.type

        if name in self.logic:
            self.logic[name]()
        else:
            error = 'Unable to find a registered logic function named: {}'
            raise KeyError(error.format(name))

    def valid_request(self):
        """Validates application id matches request.

        NOTE: application_id parameter must be set on Skill class init.

        Returns:
            bool: True if valid request, False otherwise.
        """
        req_id = self.request.session.application.application_id
        return self.application_id == req_id

    def get_error_response(self, msg='Unknown'):
        """Returns an internal server error message.

        Args:
            msg: str, default is Unknown. Error message.

        Returns:
            str: JSON formatted error message.
        """
        return """{{"InternalServerError":"{}"}}""".format(msg)

    def process(self, body):
        """Process request body given skill logic.

        Attributes received through body will be automatically added to the
            response.

        Args:
            body: dict. HTTP request body. If str is passed, attempts conversion
                to dict.

        Return:
            str: HTTP response body.
        """
        self.request = RequestBody()
        self.response = ResponseBody()

        self.request.parse(body)

        if self.application_id:
            if not self.valid_request():
                return self.get_error_response('invalid application_id')

        self.pass_attributes()

        self.dispatch()

        if self.request.request.type == 'SessionEndedRequest':
            self.terminate()

        return self.response.to_json()
