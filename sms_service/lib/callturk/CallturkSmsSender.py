#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sms_service.Errors import ErrorTypeError, ErrorTokenExpired, ErrorWebServiceError
from sms_service.Interfaces import InterfaceSmsSenderAdapter
from .EnumCallturkEndpoints import EnumCallturkEndpoint
from .xml.authentication.AuthenticationXmlController import AuthenticationXmlController
from .xml.sms_send.SmsSendController import SmsSendXmlController


class CallturkSmsSender(InterfaceSmsSenderAdapter):
    error_auth_instance = "`self.call_turk_auth` should be instance of `AuthenticationXmlController` not {}"
    error_number_list_instance = '`number_list` type is should be `list` not {}'
    REGISTERED_TOKENS = {}

    def __init__(self, username=None, password=None, organization_name=None):
        """
        (string, string, string) -> instance

        :param username: Callturk Username
        :param password: Callturk Userpassword
        :param organization_name: Calltruk Company Name
        """
        self.call_turk_auth = AuthenticationXmlController(username, password, organization_name)
        self.registered_token_key = "{}-{}".format(username, organization_name)
        self.sms_sender_ctrl = None
        self.response_tuple = {}, -1

    def send_sms(self):
        try:
            self.auth_token = CallturkSmsSender.REGISTERED_TOKENS.get(self.registered_token_key, None)
            self.sms_sender_ctrl = SmsSendXmlController(self.auth_token, self.number_list, self.content)
            sms_send_request_id = self.sms_sender_ctrl.send_sms()
            self.response_tuple = self.handle_sms_response(sms_send_request_id), 201
        except ErrorTokenExpired:
            del self.auth_token
            return self.send_sms()
        except ErrorWebServiceError as e:
            self.response_tuple = self.handle_sms_error_response(e), 200
        return self.response_tuple

    def handle_sms_response(self, response):
        return dict(id=response)

    def handle_sms_error_response(self, exception):
        return dict(
            message=exception.__class__.__name__,
            description=str(exception),
            errors=list(exception.args),
            status_code=200
        )

    def get_log_data(self):
        """  VOID

        Log sms actions
        """
        return dict(
            method='POST',
            url='{}'.format(EnumCallturkEndpoint.SMS_SEND.value),
            body=dict(number_list=self.number_list, content=self.content),
            is_failed=False if self.response_tuple[1] == 201 else True,
            status_code=self.response_tuple[1],
            response=[self.response_tuple[0]]
        )

    @property
    def auth_token(self):
        return self.__auth_token

    @auth_token.setter
    def auth_token(self, value):
        if isinstance(value, str):
            self.__auth_token = value
            CallturkSmsSender.REGISTERED_TOKENS.update({self.registered_token_key: value})
        else:
            self.auth_token = self.call_turk_auth.get_auth_token()

    @auth_token.deleter
    def auth_token(self):
        del self.__auth_token
        del CallturkSmsSender.REGISTERED_TOKENS[self.registered_token_key]

    @property
    def call_turk_auth(self):
        return self.__auth

    @call_turk_auth.setter
    def call_turk_auth(self, value):
        if not isinstance(value, AuthenticationXmlController):
            raise TypeError(CallturkSmsSender.error_auth_instance.format(type(value)))
        self.__auth = value

    @property
    def number_list(self):
        return self.__number_list

    @number_list.setter
    def number_list(self, number_list):
        if not isinstance(number_list, list):
            raise ErrorTypeError(CallturkSmsSender.error_number_list_instance.format(type(number_list)))
        self.__number_list = number_list

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, sms_content):
        self.__content = sms_content
