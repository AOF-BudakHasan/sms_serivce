
import os
import requests
from xml.etree import ElementTree as ET
from sms_service.Interfaces import InterfaceXmlController
from sms_service.lib.callturk import XmlResponseHandler
from sms_service.lib.callturk.EnumCallturkEndpoints import EnumCallturkEndpoint

__all__ = ['AuthenticationXmlController']


class AuthenticationXmlController(InterfaceXmlController):
    xml_path = os.path.join('sms_service', 'lib', 'callturk', 'xml', 'authentication', "authenticate.request.xml")
    error_xml_type = "`self.xml` property should be instance of ElementTree not {}"
    error_response_xml_type = "`self.response_xml` property should be instance of ElementTree.Element not {}"

    def __init__(self, username=None, password=None, organization_name=None):
        self.xml = ET.parse(AuthenticationXmlController.xml_path)
        self.xml_root = self.xml.getroot()
        self.username = username
        self.password = password
        self.organization_name = organization_name
        self.headers = {
            'Content-Type': 'application/xml',
            'QR-Request-Type': 'Authentication'
        }

    def get_as_string(self):
        return ET.tostring(self.xml_root, encoding='utf-8', method='xml')

    def get_auth_token(self):
        return self.handle_auth_response(self.request_auth_token())

    def request_auth_token(self):
        return requests.post(
            url=EnumCallturkEndpoint.AUTH.value,
            data=self.get_as_string(),
            headers=self.headers
        )

    def handle_auth_response(self, response):
        self.response_xml = XmlResponseHandler.xml_response_handler(response)
        return self.response_xml.find('authenticationTokenId').text

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value
        self.xml_root.find('username').text = value

    @property
    def password(self):
        return self.__username

    @password.setter
    def password(self, value):
        self.__password = value
        self.xml_root.find('password').text = value

    @property
    def organization_name(self):
        return self.__username

    @organization_name.setter
    def organization_name(self, value):
        self.__organization_name = value
        self.xml_root.find('clientOrganizationUnitName').text = value

    @property
    def xml(self):
        return self.__xml

    @xml.setter
    def xml(self, value):
        if not isinstance(value, ET.ElementTree):
            raise TypeError(AuthenticationXmlController.error_xml_type.format(type(value)))
        self.__xml = value

    @property
    def response_xml(self):
        return self.__response_xml

    @response_xml.setter
    def response_xml(self, value):
        if not isinstance(value, ET.Element):
            raise TypeError(AuthenticationXmlController.error_response_xml_type.format(type(value)))
        self.__response_xml = value
