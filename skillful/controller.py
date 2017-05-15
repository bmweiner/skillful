"""Handler for request processing"""

from __future__ import absolute_import, division, print_function
from functools import wraps
import six

from .interface import RequestBody
from .interface import ResponseBody
from .interface import error_response
from .validate import Valid


class Skill(object):
    """Class for parsing, validation, logic registering, and dispatch.

    References:
        - JSON Interface Reference for Custom Skills: https://goo.gl/JpVGm4.
        - Providing Home Cards for the Amazon Alexa App: https://goo.gl/mX9P5o.
        - Speech Synthesis Markup Language (SSML) Reference: https://goo.gl/2BHQjz.

    Attributes:
        valid: skillful.validate.Valid. Request validator.
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
    def __init__(self, app_id=None):
        """Inits a Skill class with proxy request and response.

        Args:
            app_id: str, default None. Skill application ID, declare
                to validate against application ID in the request.
        """
        self.valid = Valid(app_id)
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

    def pass_session_attributes(self):
        """Copies request attributes to response"""
        for key, value in six.iteritems(self.request.session.attributes):
            self.response.sessionAttributes[key] = value

    def terminate(self):
        """Convenience function to call response.set_end_session True."""
        self.response.set_end_session(True)

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

    def process(self, body, url=None, sig=None):
        """Process request body given skill logic.

        To validate a request, both, url and sig are required.

        Attributes received through body will be automatically added to the
            response.

        Args:
            body: str. HTTP request body.
            url: str. SignatureCertChainUrl header value sent by request.
                PEM-encoded X.509 certificate chain that Alexa used to sign the
                message.
            sig: str. Signature header value sent by request. Base64-encoded
                signature of the request body.

        Return:
            str or bool: HTTP response body or False if the request is invalid.
        """
        self.request = RequestBody()
        self.response = ResponseBody()

        self.request.parse(body)

        app_id = self.request.session.application.application_id
        stamp = self.request.request.timestamp
        if not self.valid.request(app_id, body, stamp, url, sig):
            return False

        self.pass_session_attributes()

        self.dispatch()

        if self.request.request.type == 'SessionEndedRequest':
            self.terminate()

        return self.response.to_json()
