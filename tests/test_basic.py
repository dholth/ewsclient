import ewsclient
import os
import suds.client
from suds.transport.https import WindowsHttpAuthenticated

def test_basic():
    domain = os.environ.get('EWS_DOMAIN')
    username = os.environ.get('EWS_USER')
    password = os.environ.get('EWS_PASS')

    transport = WindowsHttpAuthenticated(username=username,
            password=password)
    client = suds.client.Client("https://%s/EWS/Services.wsdl" % domain,
            transport=transport,
            plugins=[ewsclient.AddService()])

    return client
