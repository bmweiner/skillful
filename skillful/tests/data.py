"""Sample data for testing skills."""

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

INVALID_CERT = """
-----BEGIN CERTIFICATE-----
MIIFGzCCBAOgAwIBAgIQe8yiyiM0iKNWtiGrwbKQGzANBgkqhkiG9w0BAQUFADCB
tTELMAkGA1UEBhMCVVMxFzAVBgNVBAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQL
ExZWZXJpU2lnbiBUcnVzdCBOZXR3b3JrMTswOQYDVQQLEzJUZXJtcyBvZiB1c2Ug
YXQgaHR0cHM6Ly93d3cudmVyaXNpZ24uY29tL3JwYSAoYykxMDEvMC0GA1UEAxMm
VmVyaVNpZ24gQ2xhc3MgMyBTZWN1cmUgU2VydmVyIENBIC0gRzMwHhcNMTUwMTMx
MDAwMDAwWhcNMTUxMDMxMjM1OTU5WjBtMQswCQYDVQQGEwJVUzETMBEGA1UECBMK
V2FzaGluZ3RvbjEQMA4GA1UEBxQHU2VhdHRsZTEZMBcGA1UEChQQQW1hem9uLmNv
bSwgSW5jLjEcMBoGA1UEAxQTZWNoby1hcGkuYW1hem9uLmNvbTCCASIwDQYJKoZI
hvcNAQEBBQADggEPADCCAQoCggEBAJ7SGV+5dY+3DRrB7nRHNUaSXtDgQ3/DywsH
BJAfxhOJbzgMYpo9LqUQ2ZR09ajX5pPPjVBg4qPoeHGNWUMVUSNO3UQKqjIThUji
+wYBi+GJXT1ZlT0C9I9e8W13Hby/ESxErAI0rpDTAB+Iuq2CawZdRISrlOOfvwMS
vFCLA54CCf9yFnq/wxCZZ567zp+PfvAhNqbFZk/jLJEO3ZuV67bvF5o7DgWiR9oV
FuJ79iIgxGgFZJeUlrKyIAI634aX32KOGLzZ+ipsVLjOg/b6rzRZm08iw+U2kFSB
QSQbn7YA6bpbw/PW5xRoB1J1miHUceiCqLsL4MnQt0JcoribXp8CAwEAAaOCAWww
ggFoMB4GA1UdEQQXMBWCE2VjaG8tYXBpLmFtYXpvbi5jb20wCQYDVR0TBAIwADAO
BgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMGUG
A1UdIAReMFwwWgYKYIZIAYb4RQEHNjBMMCMGCCsGAQUFBwIBFhdodHRwczovL2Qu
c3ltY2IuY29tL2NwczAlBggrBgEFBQcCAjAZGhdodHRwczovL2Quc3ltY2IuY29t
L3JwYTAfBgNVHSMEGDAWgBQNRFwWU0TBgn4dIKsl9AFj2L55pTArBgNVHR8EJDAi
MCCgHqAchhpodHRwOi8vc2Quc3ltY2IuY29tL3NkLmNybDBXBggrBgEFBQcBAQRL
MEkwHwYIKwYBBQUHMAGGE2h0dHA6Ly9zZC5zeW1jZC5jb20wJgYIKwYBBQUHMAKG
Gmh0dHA6Ly9zZC5zeW1jYi5jb20vc2QuY3J0MA0GCSqGSIb3DQEBBQUAA4IBAQA7
aLx3H1brQcil1MpNSkyV4RwUdx8VvbysPc4toAg402dBJQLjDqD4eYLEg7hdtTfj
AEyvuPpWmUA79UIZwyKhHcnRUU+kd68w53ibjBPlVS7irE0d3e1RheLhyIhUClMK
lQA/uEfnXgNjbwjI4kxP6564IwL5LE1FksZhNqNQrCIt0D3c1cXvJn2+CZvyZQoO
n3plmaSul1OnbvBoO6r8OI5nLCecebD8ansKJTTpCj5qtHj7rJgp4BkS3nvNd3JV
h7oNUM9hXgk3Dypd8nkmZoYG5DQo+qAbvWribFPL96bLb34q94oH9f9SCnIQZstc
VQEvq/IRMyDXwoTIEBaD
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIF7DCCBNSgAwIBAgIQbsx6pacDIAm4zrz06VLUkTANBgkqhkiG9w0BAQUFADCB
yjELMAkGA1UEBhMCVVMxFzAVBgNVBAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQL
ExZWZXJpU2lnbiBUcnVzdCBOZXR3b3JrMTowOAYDVQQLEzEoYykgMjAwNiBWZXJp
U2lnbiwgSW5jLiAtIEZvciBhdXRob3JpemVkIHVzZSBvbmx5MUUwQwYDVQQDEzxW
ZXJpU2lnbiBDbGFzcyAzIFB1YmxpYyBQcmltYXJ5IENlcnRpZmljYXRpb24gQXV0
aG9yaXR5IC0gRzUwHhcNMTAwMjA4MDAwMDAwWhcNMjAwMjA3MjM1OTU5WjCBtTEL
MAkGA1UEBhMCVVMxFzAVBgNVBAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQLExZW
ZXJpU2lnbiBUcnVzdCBOZXR3b3JrMTswOQYDVQQLEzJUZXJtcyBvZiB1c2UgYXQg
aHR0cHM6Ly93d3cudmVyaXNpZ24uY29tL3JwYSAoYykxMDEvMC0GA1UEAxMmVmVy
aVNpZ24gQ2xhc3MgMyBTZWN1cmUgU2VydmVyIENBIC0gRzMwggEiMA0GCSqGSIb3
DQEBAQUAA4IBDwAwggEKAoIBAQCxh4QfwgxF9byrJZenraI+nLr2wTm4i8rCrFbG
5btljkRPTc5v7QlK1K9OEJxoiy6Ve4mbE8riNDTB81vzSXtig0iBdNGIeGwCU/m8
f0MmV1gzgzszChew0E6RJK2GfWQS3HRKNKEdCuqWHQsV/KNLO85jiND4LQyUhhDK
tpo9yus3nABINYYpUHjoRWPNGUFP9ZXse5jUxHGzUL4os4+guVOc9cosI6n9FAbo
GLSa6Dxugf3kzTU2s1HTaewSulZub5tXxYsU5w7HnO1KVGrJTcW/EbGuHGeBy0RV
M5l/JJs/U0V/hhrzPPptf4H1uErT9YU3HLWm0AnkGHs4TvoPAgMBAAGjggHfMIIB
2zA0BggrBgEFBQcBAQQoMCYwJAYIKwYBBQUHMAGGGGh0dHA6Ly9vY3NwLnZlcmlz
aWduLmNvbTASBgNVHRMBAf8ECDAGAQH/AgEAMHAGA1UdIARpMGcwZQYLYIZIAYb4
RQEHFwMwVjAoBggrBgEFBQcCARYcaHR0cHM6Ly93d3cudmVyaXNpZ24uY29tL2Nw
czAqBggrBgEFBQcCAjAeGhxodHRwczovL3d3dy52ZXJpc2lnbi5jb20vcnBhMDQG
A1UdHwQtMCswKaAnoCWGI2h0dHA6Ly9jcmwudmVyaXNpZ24uY29tL3BjYTMtZzUu
Y3JsMA4GA1UdDwEB/wQEAwIBBjBtBggrBgEFBQcBDARhMF+hXaBbMFkwVzBVFglp
bWFnZS9naWYwITAfMAcGBSsOAwIaBBSP5dMahqyNjmvDz4Bq1EgYLHsZLjAlFiNo
dHRwOi8vbG9nby52ZXJpc2lnbi5jb20vdnNsb2dvLmdpZjAoBgNVHREEITAfpB0w
GzEZMBcGA1UEAxMQVmVyaVNpZ25NUEtJLTItNjAdBgNVHQ4EFgQUDURcFlNEwYJ+
HSCrJfQBY9i+eaUwHwYDVR0jBBgwFoAUf9Nlp8Ld7LvwMAnzQzn6Aq8zMTMwDQYJ
KoZIhvcNAQEFBQADggEBAAyDJO/dwwzZWJz+NrbrioBL0aP3nfPMU++CnqOh5pfB
WJ11bOAdG0z60cEtBcDqbrIicFXZIDNAMwfCZYP6j0M3m+oOmmxw7vacgDvZN/R6
bezQGH1JSsqZxxkoor7YdyT3hSaGbYcFQEFn0Sc67dxIHSLNCwuLvPSxe/20majp
dirhGi2HbnTTiN0eIsbfFrYrghQKlFzyUOyvzv9iNw2tZdMGQVPtAhTItVgooazg
W+yzf5VK+wPIrSbb5mZ4EkrZn0L74ZjmQoObj49nJOhhGbXdzbULJgWOw27EyHW4
Rs/iGAZeqa6ogZpHFt4MKGwlJ7net4RYxh84HqTEy2Y=
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIExjCCBC+gAwIBAgIQNZcxh/OHOgcyfs5YDJt+2jANBgkqhkiG9w0BAQUFADBf
MQswCQYDVQQGEwJVUzEXMBUGA1UEChMOVmVyaVNpZ24sIEluYy4xNzA1BgNVBAsT
LkNsYXNzIDMgUHVibGljIFByaW1hcnkgQ2VydGlmaWNhdGlvbiBBdXRob3JpdHkw
HhcNMDYxMTA4MDAwMDAwWhcNMjExMTA3MjM1OTU5WjCByjELMAkGA1UEBhMCVVMx
FzAVBgNVBAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQLExZWZXJpU2lnbiBUcnVz
dCBOZXR3b3JrMTowOAYDVQQLEzEoYykgMjAwNiBWZXJpU2lnbiwgSW5jLiAtIEZv
ciBhdXRob3JpemVkIHVzZSBvbmx5MUUwQwYDVQQDEzxWZXJpU2lnbiBDbGFzcyAz
IFB1YmxpYyBQcmltYXJ5IENlcnRpZmljYXRpb24gQXV0aG9yaXR5IC0gRzUwggEi
MA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCvJAgIKXo1nmAMqudLO07cfLw8
RRy7K+D+KQL5VwijZIUVJ/XxrcgxiV0i6CqqpkKzj/i5Vbext0uz/o9+B1fs70Pb
ZmIVYc9gDaTY3vjgw2IIPVQT60nKWVSFJuUrjxuf6/WhkcIzSdhDY2pSS9KP6HBR
TdGJaXvHcPaz3BJ023tdS1bTlr8Vd6Gw9KIl8q8ckmcY5fQGBO+QueQA5N06tRn/
Arr0PO7gi+s3i+z016zy9vA9r911kTMZHRxAy3QkGSGT2RT+rCpSx4/VBEnkjWNH
iDxpg8v+R70rfk/Fla4OndTRQ8Bnc+MUCH7lP59zuDMKz10/NIeWiu5T6CUVAgMB
AAGjggGRMIIBjTAPBgNVHRMBAf8EBTADAQH/MDEGA1UdHwQqMCgwJqAkoCKGIGh0
dHA6Ly9jcmwudmVyaXNpZ24uY29tL3BjYTMuY3JsMA4GA1UdDwEB/wQEAwIBBjA9
BgNVHSAENjA0MDIGBFUdIAAwKjAoBggrBgEFBQcCARYcaHR0cHM6Ly93d3cudmVy
aXNpZ24uY29tL2NwczAdBgNVHQ4EFgQUf9Nlp8Ld7LvwMAnzQzn6Aq8zMTMwNAYD
VR0lBC0wKwYJYIZIAYb4QgQBBgpghkgBhvhFAQgBBggrBgEFBQcDAQYIKwYBBQUH
AwIwbQYIKwYBBQUHAQwEYTBfoV2gWzBZMFcwVRYJaW1hZ2UvZ2lmMCEwHzAHBgUr
DgMCGgQUj+XTGoasjY5rw8+AatRIGCx7GS4wJRYjaHR0cDovL2xvZ28udmVyaXNp
Z24uY29tL3ZzbG9nby5naWYwNAYIKwYBBQUHAQEEKDAmMCQGCCsGAQUFBzABhhho
dHRwOi8vb2NzcC52ZXJpc2lnbi5jb20wDQYJKoZIhvcNAQEFBQADgYEADyWuSO0b
M4VMDLXC1/5N1oMoTEFlYAALd0hxgv5/21oOIMzS6ke8ZEJhRDR0MIGBJopK90Rd
fjSAqLiD4gnXbSPdie0oCL1jWhFXCMSe2uJoKK/dUDzsgiHYAMJVRFBwQa2DF3m6
CPMr3u00HUSe0gST9MsFFy0JLS1j7/YmC3s=
-----END CERTIFICATE-----
"""

VALID_CERT = """
-----BEGIN CERTIFICATE-----
MIIFfjCCBGagAwIBAgIQPyXKruWqg4+pHAUadfxxnTANBgkqhkiG9w0BAQsFADB+
MQswCQYDVQQGEwJVUzEdMBsGA1UEChMUU3ltYW50ZWMgQ29ycG9yYXRpb24xHzAd
BgNVBAsTFlN5bWFudGVjIFRydXN0IE5ldHdvcmsxLzAtBgNVBAMTJlN5bWFudGVj
IENsYXNzIDMgU2VjdXJlIFNlcnZlciBDQSAtIEc0MB4XDTE2MTAwNzAwMDAwMFoX
DTE3MTAzMDIzNTk1OVowbTELMAkGA1UEBhMCVVMxEzARBgNVBAgMCldhc2hpbmd0
b24xEDAOBgNVBAcMB1NlYXR0bGUxGTAXBgNVBAoMEEFtYXpvbi5jb20sIEluYy4x
HDAaBgNVBAMME2VjaG8tYXBpLmFtYXpvbi5jb20wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQCcr7MGu5EDVOduBAbET5vheJNNnIOQbAnrTrwAaxdCaC32
VWELwJNMLjB1Hk1eixuhXr/rfCitAI2jjXZywFWNTLcfX9USz7kq/4CIA5S4qgF8
RTzMC8cJzsaY4pSA2J1wMDQxKnHdlMxIYZuR9ouKRHOd7qcVnqM06eSpO0YPpKsI
hiAs0CtJxig/MhxcTKkcWuiCfOtHgR7Rhx58ZnJLzVip6/+WWLTV0CBG+mcC3Lry
thObGQ2HNRIboghsUcjFckoARMCQaIolyBml8bbU6TkOTfIasRJj8gPk6fG8zGJd
KdfCG3wkPpt3Xm6LS08NrzkHSOlkuWipBl7bqhGjAgMBAAGjggIHMIICAzAeBgNV
HREEFzAVghNlY2hvLWFwaS5hbWF6b24uY29tMAkGA1UdEwQCMAAwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjBhBgNVHSAEWjBY
MFYGBmeBDAECAjBMMCMGCCsGAQUFBwIBFhdodHRwczovL2Quc3ltY2IuY29tL2Nw
czAlBggrBgEFBQcCAjAZDBdodHRwczovL2Quc3ltY2IuY29tL3JwYTAfBgNVHSME
GDAWgBRfYM9hkFXfhEMUimAqsvV69EMY7zArBgNVHR8EJDAiMCCgHqAchhpodHRw
Oi8vc3Muc3ltY2IuY29tL3NzLmNybDBXBggrBgEFBQcBAQRLMEkwHwYIKwYBBQUH
MAGGE2h0dHA6Ly9zcy5zeW1jZC5jb20wJgYIKwYBBQUHMAKGGmh0dHA6Ly9zcy5z
eW1jYi5jb20vc3MuY3J0MA8GAytlTQQIMAYCAQECAQEwgYsGCisGAQQB1nkCBAIE
fQR7AHkAdwCnzkpOYgfgrd7l/apLH4Z2h2e10AKlXUcxDn5nCpXqsgAAAVefqkBK
AAAEAwBIMEYCIQDKa3wGnBQLd06NZO2V1KWekjSeBKo8cbME8yx0vIV/gQIhAPoV
LPhVi6Coe1Fat1ItG+FyV0DhKAQjCd0nT+6l6ztiMA0GCSqGSIb3DQEBCwUAA4IB
AQB7hqbnqGsZJXk4AQi36tocJeKIq0YSARfcaoBjUyTIlxPHAgbvP+E8yl7f9DYB
lyy5ZliCatzWiw+zrn9WB9A21q6K+CTNltfxtNtY5xQ0MDHykrF+bu+DhyoP1YbM
DR2oWmd+SrTGVA6RMrW8VkRTPgOI+DCxtnV7fbiKuChG8Is7bc7H8kMZq36lb4ZZ
Ld3sRSLK8zHIuBpOVD+9v01mG1NLrlRkZduIpSW8gqe0En8K/0pVUlknpmoJBVdD
8QnjDZDKB00lgWbw5HLLfM2wdHredPcEDP7rmnjDSDhkxRBtVCVWyHSvdoAFpuyD
resu4y+Ob3GCo2J3XCv0Cvog
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIFODCCBCCgAwIBAgIQUT+5dDhwtzRAQY0wkwaZ/zANBgkqhkiG9w0BAQsFADCB
yjELMAkGA1UEBhMCVVMxFzAVBgNVBAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQL
ExZWZXJpU2lnbiBUcnVzdCBOZXR3b3JrMTowOAYDVQQLEzEoYykgMjAwNiBWZXJp
U2lnbiwgSW5jLiAtIEZvciBhdXRob3JpemVkIHVzZSBvbmx5MUUwQwYDVQQDEzxW
ZXJpU2lnbiBDbGFzcyAzIFB1YmxpYyBQcmltYXJ5IENlcnRpZmljYXRpb24gQXV0
aG9yaXR5IC0gRzUwHhcNMTMxMDMxMDAwMDAwWhcNMjMxMDMwMjM1OTU5WjB+MQsw
CQYDVQQGEwJVUzEdMBsGA1UEChMUU3ltYW50ZWMgQ29ycG9yYXRpb24xHzAdBgNV
BAsTFlN5bWFudGVjIFRydXN0IE5ldHdvcmsxLzAtBgNVBAMTJlN5bWFudGVjIENs
YXNzIDMgU2VjdXJlIFNlcnZlciBDQSAtIEc0MIIBIjANBgkqhkiG9w0BAQEFAAOC
AQ8AMIIBCgKCAQEAstgFyhx0LbUXVjnFSlIJluhL2AzxaJ+aQihiw6UwU35VEYJb
A3oNL+F5BMm0lncZgQGUWfm893qZJ4Itt4PdWid/sgN6nFMl6UgfRk/InSn4vnlW
9vf92Tpo2otLgjNBEsPIPMzWlnqEIRoiBAMnF4scaGGTDw5RgDMdtLXO637QYqzu
s3sBdO9pNevK1T2p7peYyo2qRA4lmUoVlqTObQJUHypqJuIGOmNIrLRM0XWTUP8T
L9ba4cYY9Z/JJV3zADreJk20KQnNDz0jbxZKgRb78oMQw7jW2FUyPfG9D72MUpVK
Fpd6UiFjdS8W+cRmvvW1Cdj/JwDNRHxvSz+w9wIDAQABo4IBYzCCAV8wEgYDVR0T
AQH/BAgwBgEB/wIBADAwBgNVHR8EKTAnMCWgI6Ahhh9odHRwOi8vczEuc3ltY2Iu
Y29tL3BjYTMtZzUuY3JsMA4GA1UdDwEB/wQEAwIBBjAvBggrBgEFBQcBAQQjMCEw
HwYIKwYBBQUHMAGGE2h0dHA6Ly9zMi5zeW1jYi5jb20wawYDVR0gBGQwYjBgBgpg
hkgBhvhFAQc2MFIwJgYIKwYBBQUHAgEWGmh0dHA6Ly93d3cuc3ltYXV0aC5jb20v
Y3BzMCgGCCsGAQUFBwICMBwaGmh0dHA6Ly93d3cuc3ltYXV0aC5jb20vcnBhMCkG
A1UdEQQiMCCkHjAcMRowGAYDVQQDExFTeW1hbnRlY1BLSS0xLTUzNDAdBgNVHQ4E
FgQUX2DPYZBV34RDFIpgKrL1evRDGO8wHwYDVR0jBBgwFoAUf9Nlp8Ld7LvwMAnz
Qzn6Aq8zMTMwDQYJKoZIhvcNAQELBQADggEBAF6UVkndji1l9cE2UbYD49qecxny
H1mrWH5sJgUs+oHXXCMXIiw3k/eG7IXmsKP9H+IyqEVv4dn7ua/ScKAyQmW/hP4W
Ko8/xabWo5N9Q+l0IZE1KPRj6S7t9/Vcf0uatSDpCr3gRRAMFJSaXaXjS5HoJJtG
QGX0InLNmfiIEfXzf+YzguaoxX7+0AjiJVgIcWjmzaLmFN5OUiQt/eV5E1PnXi8t
TRttQBVSK/eHiXgSgW7ZTaoteNTCLD0IX4eRnh8OsN4wUmSGiaqdZpwOdgyA8nTY
Kvi4Os7X1g8RvmurFPW9QaAiY4nxug9vKWNmLT+sjHLF+8fk1A/yO0+MKcc=
-----END CERTIFICATE-----
"""

CORRUPT_CERT = """
-----BEGIN CERTIFICATE-----
MIIFGzCCBAOgAwIBAgIQe8yiyiM0iKNWtiGrwbKQGzANBgkqhkiG9w0BAQUFADCB
tTELMAkGA1UEBhMCVVMxFzAVBgNVBAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQL
ExZWZXJpU2lnbiBUcnVzdCBOZXR3b3JrMTswOQYDVQQLEzJUZXJtcyBvZiB1c2Ug
YXQgaHR0cHM6Ly93d3cudmVyaXNpZ24uY29tL3JwYSAoYykxMDEvMC0GA1UEAxMm
VmVyaVNpZ24gQ2xhc3MgMyBTZWN1cmUgU2VydmVyIENBIC0gRzMwHhcNMTUwMTMx
MDAwMDAwWhcNMTUxMDMxMjM1OTU5WjBtMQswCQYDVQQGEwJVUzETMBEGA1UECBMK
V2FzaGluZ3RvbjEQMA4GA1UEBxQHU2VhdHRsZTEZMBcGA1UEChQQQW1hem9uLmNv
bSwgSW5jLjEcMBoGA1UEAxQTZWNoby1hcGkuYW1hem9uLmNvbTCCASIwDQYJKoZI
hvcNAQEBBQADggEPADCCAQoCggEBAJ7SGV+5dY+3DRrB7nRHNUaSXtDgQ3/DywsH
BJAfxhOJbzgMYpo9LqUQ2ZR09ajX5pPPjVBg4qPoeHGNWUMVUSNO3UQKqjIThUji
+wYBi+GJXT1ZlT0C9I9e8W13Hby/ESxErAI0rpDTAB+Iuq2CawZdRISrlOOfvwMS
-----END CERTIFICATE-----
"""
