"""Handler for request validation"""


import warnings
import os
import sys
import datetime
import base64
import six
from six.moves.urllib_parse import urlparse
from six.moves.urllib.request import urlopen
from six.moves.urllib_error import HTTPError
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import dateutil.parser


def timestamp(stamp, tolerance=150):
    """Validate timestamp specified by request.

    See `validate.request` for additional info.

    Args:
        stamp: str. Time request was made as ISO 8601 timestamp.
        tolerance: int. Number of seconds request remains valid from timestamp.

    Returns
        bool: True if valid, False otherwise.
    """
    try:
        tolerance = datetime.timedelta(0, tolerance)
        timestamp_low = dateutil.parser.parse(stamp)
        timestamp_high = timestamp_low + tolerance
        now = datetime.datetime.now(timestamp_low.tzinfo)
    except ValueError:
        return False

    return now >= timestamp_low and now <= timestamp_high

def signature_cert_chain_url(url):
    """Validate URL specified by SignatureCertChainUrl.

    See `validate.request` for additional info.

    Args:
        url: str. SignatureCertChainUrl header value sent by request.

    Returns:
        bool: True if valid, False otherwise.
    """
    r = urlparse(url)
    if not r.scheme.lower() == 'https':
        warnings.warn('Certificate URL scheme is invalid.')
        return False
    if not r.hostname.lower() == 's3.amazonaws.com':
        warnings.warn('Certificate URL hostname is invalid.')
        return False
    if not os.path.normpath(r.path).startswith('/echo.api/'):
        warnings.warn('Certificate URL path is invalid.')
        return False
    if r.port and not r.port == 443:
        warnings.warn('Certificate URL port is invalid.')
        return False
    return True

def retrieve(url):
    """Retrieve and parse PEM-encoded X.509 certificate chain.

    See `validate.request` for additional info.

    Args:
        url: str. SignatureCertChainUrl header value sent by request.

    Returns:
        list or bool: If url is valid, returns the certificate chain as a list
            of cryptography.hazmat.backends.openssl.x509._Certificate
            certificates where certs[0] is the first certificate in the file; if
            url is invalid, returns False.
    """
    try:
        pem_data = urlopen(url).read()
    except (ValueError, HTTPError):
        warnings.warn('Certificate URL is invalid.')
        return False

    if sys.version >= '3':
        try:
            pem_data = pem_data.decode()
        except(UnicodeDecodeError):
            warnings.warn('Certificate encoding is not utf-8.')
            return False

    return _parse_pem_data(pem_data)

def _parse_pem_data(pem_data):
    """Parse PEM-encoded X.509 certificate chain.

    Args:
        pem_data: str. PEM file retrieved from SignatureCertChainUrl.

    Returns:
        list or bool: If url is valid, returns the certificate chain as a list
            of cryptography.hazmat.backends.openssl.x509._Certificate
            certificates where certs[0] is the first certificate in the file; if
            url is invalid, returns False.
    """
    sep = '-----BEGIN CERTIFICATE-----'
    cert_chain = [six.b(sep + s) for s in pem_data.split(sep)[1:]]
    certs = []
    load_cert = x509.load_pem_x509_certificate
    for cert in cert_chain:
        try:
            certs.append(load_cert(cert, default_backend()))
        except ValueError:
            warnings.warn('Certificate is invalid.')
            return False

    return certs

def cert_chain(certs):
    """Validate PEM-encoded X.509 certificate chain.

    See `validate.request` for additional info.

    Args:
        certs: list. The certificate chain as a list of
            cryptography.hazmat.backends.openssl.x509._Certificate certificates.
            See `validate.retrieve` to create certs obj.

    Returns:
        bool: True if valid, False otherwise.
    """
    if len(certs) < 2:
        warnings.warn('Certificate chain contains < 3 certificates.')
        return False

    cert = certs[0]
    today = datetime.datetime.today()
    if not today > cert.not_valid_before:
        warnings.warn('Certificate Not Before date is invalid.')
        return False
    if not today < cert.not_valid_after:
        warnings.warn('Certificate Not After date is invalid.')
        return False

    oid_san = x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME
    ext = cert.extensions.get_extension_for_oid(oid_san)
    sans = ext.value.get_values_for_type(x509.DNSName)
    if not 'echo-api.amazon.com' in sans:
        return False

    for i in range(len(certs) - 1):
        if not certs[i].issuer == certs[i + 1].subject:
            return False

    return True

def signature(cert, sig, body):
    """Validate data request signature.

    See `validate.request` for additional info.

    Args:
        cert: cryptography.hazmat.backends.openssl.x509._Certificate. The Amazon
            signing certificate.
        sig: str. Signature header value sent by request.
        body: str. HTTPS request body.

    Returns:
        bool: True if valid, False otherwise.
    """
    body = six.b(body)

    sig = base64.decodestring(sig)
    padder = padding.PKCS1v15()
    public_key = cert.public_key()
    try:
        public_key.verify(sig, body, padder, hashes.SHA1())
        return True
    except InvalidSignature:
        warnings.warn('Signature verification failed.')
        return False

class Valid(object):
    """Alexa request validator.

    Attributes:
        app_id: str. Skill application ID.
        url: str. SignatureCertChainUrl header value sent by request.
            PEM-encoded X.509 certificate chain that Alexa used to sign the
            message. Used to cache valid url.
        cert: cryptography.hazmat.backends.openssl.x509._Certificate. The Amazon
            signing certificate. Used to cache valid cert.
    """
    def __init__(self, app_id=None):
        """Init validator."""
        self.app_id = app_id
        self.url = None
        self.cert = None

    def application_id(self, app_id):
        """Validate request application id matches true application id.

        Verifying the Application ID matches: https://goo.gl/qAdqe4.

        Args:
            app_id: str. Request application_id.

        Returns:
            bool: True if valid, False otherwise.
        """
        if self.app_id != app_id:
            warnings.warn('Application ID is invalid.')
            return False
        return True

    def sender(self, body, stamp, url, sig):
        """Validate request is from Alexa.

        Verifying that the Request was Sent by Alexa: https://goo.gl/AcrzB5.
        Checking the Signature of the Request: https://goo.gl/FDkjBN.
        Checking the Timestamp of the Request: https://goo.gl/Z5JhqZ

        Args:
            body: str. HTTPS request body.
            stamp: str. Value of timestamp within request object of HTTPS
                request body.
            url: str. SignatureCertChainUrl header value sent
                by request.
            sig: str. Signature header value sent by request.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not timestamp(stamp):
            return False

        if self.url != url:
            if not signature_cert_chain_url(url):
                return False

            certs = retrieve(url)
            if not certs:
                return False

            if not cert_chain(certs):
                return False

            self.url = url
            self.cert = certs[0]

        if not signature(self.cert, sig, body):
            return False

        return True

    def request(self, app_id=None, body=None, stamp=None, url=None, sig=None):
        """Validate application ID and request is from Alexa."""
        if self.app_id:
            if not self.application_id(app_id):
                return False

        if (url or sig):
            if not (body and stamp and url and sig):
                raise ValueError('Unable to validate sender, check arguments.')
            else:
                if not self.sender(body, stamp, url, sig):
                    return False

        return True
