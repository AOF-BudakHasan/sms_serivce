
import os
import requests
from xml.etree import ElementTree as ET
from sms_service.lib.callturk import XmlResponseHandler
from sms_service.Interfaces import InterfaceXmlController
from sms_service.lib.callturk.EnumCallturkEndpoints import EnumCallturkEndpoint

__all__ = ['SmsSendXmlController']


class SmsSendXmlController(InterfaceXmlController):
    xml_path = os.path.join('sms_service', 'lib', 'callturk', 'xml', 'sms_send', "sms_send.request.xml")
    error_xml_type = "`self.xml` property should be instance of ElementTree not {}"
    error_response_xml_type = "`self.response_xml` property should be instance of ElementTree.Element not {}"

    def __init__(self, auth_token, number_list, sms_content):
        self.xml = ET.parse(SmsSendXmlController.xml_path)
        self.xml_root = self.xml.getroot()
        self.auth_token = auth_token
        self.set_content(sms_content)
        self.set_number_list(number_list)
        self.headers = {
            'Content-Type': 'application/xml',
            'authenticationTokenId': self.auth_token,
            'QR-Request-Type': 'SmsSend'
        }

    def get_as_string(self):
        return ET.tostring(self.xml_root, encoding='utf-8', method='xml')

    def set_number_list(self, number_list):
        self.xml_root.find('phoneNumberSet').clear()
        for number in number_list:
            new_element = ET.Element('phoneNumber')
            new_element.text = number
            self.xml_root.find('phoneNumberSet').append(new_element)

    def set_content(self, sms_content):
        self.xml_root.find('smsText').text = sms_content

    def send_sms(self):
        return self.handle_response(self.do_request())

    def do_request(self):
        self.headers['authenticationTokenId'] = self.auth_token
        return requests.post(
            url=EnumCallturkEndpoint.SMS_SEND.value,
            data=self.get_as_string(),
            headers=self.headers
        )

    def handle_response(self, response):
        self.response_xml = XmlResponseHandler.xml_response_handler(response)
        return self.response_xml.find('smsSendRequestId').text

    @property
    def xml(self):
        return self.__xml

    @xml.setter
    def xml(self, value):
        if not isinstance(value, ET.ElementTree):
            raise TypeError(SmsSendXmlController.error_xml_type.format(type(value)))
        self.__xml = value

    @property
    def response_xml(self):
        return self.__response_xml

    @response_xml.setter
    def response_xml(self, value):
        if not isinstance(value, ET.Element):
            raise TypeError(SmsSendXmlController.error_response_xml_type.format(type(value)))
        self.__response_xml = value
