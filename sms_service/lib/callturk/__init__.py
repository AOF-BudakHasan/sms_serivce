#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET
from sms_service.Errors import ErrorTokenExpired, ErrorWebServiceError


class XmlResponseHandler:
    @staticmethod
    def xml_response_handler(response):
        response_xml = ET.fromstring(str(response.text))
        if response.status_code == 401:
            message = 'SESSION_SERVICE.SESSION_EXPIRED'
            try:
                message = response_xml.find('responseMessage').text
            except Exception as e:
                pass
            raise ErrorTokenExpired(message)
        if response_xml.find('webServiceResponseType').text != 'SUCCESS':
            raise ErrorWebServiceError(response_xml.find('responseMessage').text)
        return response_xml

