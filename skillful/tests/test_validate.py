"""skillful validate module tests"""
# pylint: disable=protected-access
# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import os
import datetime
import base64
import unittest

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import padding

from skillful import validate
from skillful.tests import data

# setup self-signed cert for testing
certificate = {}
certificate['key'] = rsa.generate_private_key(public_exponent=65537,
    key_size=2048, backend=default_backend())

certificate['subject'] = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"CA"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com"),
    ])

certificate['cert'] = x509.CertificateBuilder().subject_name(
        certificate['subject']
    ).issuer_name(
        certificate['subject']
    ).public_key(
        certificate['key'].public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=10)
    ).sign(certificate['key'], hashes.SHA256(), default_backend())

class TestTimestamp(unittest.TestCase):
    """Test timestamp function."""
    def test_timestamp_valid(self):
        """Test valid timestamp."""
        ts = datetime.datetime.now().isoformat()
        self.assertTrue(validate.timestamp(ts))
    def test_timestamp_invalid(self):
        """Test invalid timestamp."""
        ts = '2015-05-13T12:34:56Z'
        self.assertFalse(validate.timestamp(ts))

class TestSignatureCertChainUrl(unittest.TestCase):
    """Test signature_cert_chain_url function."""
    def test_signature_cert_chain_url_valid1(self):
        """Test valid url."""
        url = "https://s3.amazonaws.com/echo.api/echo-api-cert.pem"
        self.assertTrue(validate.signature_cert_chain_url(url))

    def test_signature_cert_chain_url_valid2(self):
        """Test valid url."""
        url = "https://s3.amazonaws.com:443/echo.api/echo-api-cert.pem"
        self.assertTrue(validate.signature_cert_chain_url(url))

    def test_signature_cert_chain_url_valid3(self):
        """Test valid url."""
        url = "https://s3.amazonaws.com/echo.api/../echo.api/echo-api-cert.pem"
        self.assertTrue(validate.signature_cert_chain_url(url))

    def test_signature_cert_chain_url_invalid_scheme(self):
        """Test invalid url."""
        url = "http://s3.amazonaws.com/echo.api/echo-api-cert.pem"
        self.assertFalse(validate.signature_cert_chain_url(url))

    def test_signature_cert_chain_url_invalid_hostname(self):
        """Test invalid url."""
        url = "https://notamazon.com/echo.api/echo-api-cert.pem"
        self.assertFalse(validate.signature_cert_chain_url(url))

    def test_signature_cert_chain_url_invalid_path1(self):
        """Test invalid url."""
        url = "https://s3.amazonaws.com/EcHo.aPi/echo-api-cert.pem"
        self.assertFalse(validate.signature_cert_chain_url(url))

    def test_signature_cert_chain_url_invalid_path2(self):
        """Test invalid url."""
        url = "https://s3.amazonaws.com/invalid.path/echo-api-cert.pem"
        self.assertFalse(validate.signature_cert_chain_url(url))

    def test_signature_cert_chain_url_invalid_port(self):
        """Test invalid url."""
        url = "https://s3.amazonaws.com:563/echo.api/echo-api-cert.pem"
        self.assertFalse(validate.signature_cert_chain_url(url))

class TestRetrieve(unittest.TestCase):
    """Test retrieve function."""
    def test_retrieve_valid(self):
        """Test valid url."""
        url = "https://s3.amazonaws.com/echo.api/echo-api-cert.pem"
        self.assertTrue(validate.retrieve(url))

    def test_retrieve_invalid1(self):
        """Test invalid url."""
        url = "https://google.com"
        self.assertFalse(validate.retrieve(url))

    def test_retrieve_invalid2(self):
        """Test invalid url."""
        url = ""
        self.assertFalse(validate.retrieve(url))

class TestParsePemData(unittest.TestCase):
    """Test _parse_pem_data function."""
    def test__parse_pem_data_valid(self):
        """Test valid pem data."""
        pem_data = data.VALID_CERT
        self.assertTrue(validate._parse_pem_data(pem_data))

    def test__parse_pem_data_invalid(self):
        """Test invalid pem data."""
        pem_data = data.CORRUPT_CERT
        self.assertFalse(validate._parse_pem_data(pem_data))

class TestCertChain(unittest.TestCase):
    """Test cert_chain function."""
    def test_cert_chain_valid(self):
        """Test valid cert_chain."""
        certs = validate._parse_pem_data(data.VALID_CERT)
        self.assertTrue(validate.cert_chain(certs))

    def test_cert_chain_invalid1(self):
        """Test invalid cert_chain."""
        certs = validate._parse_pem_data(data.INVALID_CERT)
        self.assertFalse(validate.cert_chain(certs))

    def test_cert_chain_invalid2(self):
        """Test invalid cert_chain (too short)."""
        certs = validate._parse_pem_data(data.VALID_CERT)[:1]
        self.assertFalse(validate.cert_chain(certs))

class TestSignature(unittest.TestCase):
    """Test signature function."""
    @classmethod
    def setUpClass(cls):
        """Setup certificate."""
        cls.key = certificate['key']
        cls.cert = certificate['cert']

    def test_signature_valid(self):
        """Test valid signature."""
        data = 'text to encrypt'
        signature = self.key.sign(data, padding.PKCS1v15(), hashes.SHA1())
        signature = base64.encodestring(signature)
        self.assertTrue(validate.signature(self.cert, signature, data))

    def test_signature_invalid(self):
        """Test invalid signature."""
        data = 'text to encrypt'
        signature = self.key.sign(data, padding.PKCS1v15(), hashes.SHA1())
        signature = base64.encodestring(signature)
        self.assertFalse(validate.signature(self.cert, signature, data + 'a'))

class TestValid(unittest.TestCase):
    """Test Valid class."""
    @classmethod
    def setUpClass(cls):
        """Setup the class and certificate."""
        cls.valid = validate.Valid()
        cls.key = certificate['key']
        cls.cert = certificate['cert']

    def test_application_id_valid(self):
        """Test application_id method."""
        self.valid.app_id = '12345'
        self.assertTrue(self.valid.application_id('12345'))

    def test_application_id_invalid(self):
        """Test application_id method."""
        self.valid.app_id = '1'
        self.assertFalse(self.valid.application_id('2'))

    def test_sender_valid(self):
        """Test sender method."""
        self.valid.url = 'valid_url'
        self.valid.cert = self.cert

        body = 'text to encrypt'
        stamp = datetime.datetime.now().isoformat()
        url = 'valid_url'
        sig = self.key.sign(body, padding.PKCS1v15(), hashes.SHA1())
        sig = base64.encodestring(sig)

        self.assertTrue(self.valid.sender(body, stamp, url, sig))

    def test_sender_invalid_timestamp(self):
        """Test sender method bad timestamp."""
        self.valid.url = 'valid_url'
        self.valid.cert = self.cert

        body = 'text to encrypt'
        stamp = 'invalid stamp'
        url = 'valid_url'
        sig = self.key.sign(body, padding.PKCS1v15(), hashes.SHA1())
        sig = base64.encodestring(sig)

        self.assertFalse(self.valid.sender(body, stamp, url, sig))

    def test_sender_invalid_signature_cert_chain_url(self):
        """Test sender method bad signature_cert_chain_url."""
        self.valid.url = None
        self.valid.cert = self.cert

        body = 'text to encrypt'
        stamp = datetime.datetime.now().isoformat()
        url = "invalid_url"
        sig = self.key.sign(body, padding.PKCS1v15(), hashes.SHA1())
        sig = base64.encodestring(sig)

        self.assertFalse(self.valid.sender(body, stamp, url, sig))

    def test_sender_invalid_cert_chain(self):
        """Test sender method bad cert chain."""
        self.valid.url = None
        self.valid.cert = self.cert

        body = 'text to encrypt'
        stamp = datetime.datetime.now().isoformat()
        url = "https://s3.amazonaws.com/echo.api/echo-api-cert.pem"
        sig = self.key.sign(body, padding.PKCS1v15(), hashes.SHA1())
        sig = base64.encodestring(sig)

        self.assertFalse(self.valid.sender(body, stamp, url, sig))

    def test_sender_cache_invalid_signature(self):
        """Test sender method, cache with bad signature."""
        self.valid.url = None
        self.valid.cert = None

        body = 'text to encrypt'
        stamp = datetime.datetime.now().isoformat()
        url = 'https://s3.amazonaws.com/echo.api/echo-api-cert-4.pem'
        sig = self.key.sign(body, padding.PKCS1v15(), hashes.SHA1())
        sig = base64.encodestring(sig)

        self.assertFalse(self.valid.sender(body, stamp, url, sig))
        self.assertIsNotNone(self.valid.url)
        self.assertIsNotNone(self.valid.cert)
        
