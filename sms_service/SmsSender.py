#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .Errors import ErrorTypeError
from .ValidateSmsContent import ValidateSmsContent
from .Interfaces import InterfaceSetSmsAdapter, InterfaceSmsSender, InterfaceSmsSenderAdapter

__all__ = ['SmsSender', 'ValidateSmsContent']


class SmsSender(InterfaceSmsSender, InterfaceSetSmsAdapter):
    """Send text as SMS
    """
    adapter_assert_error = "Parameter `adapter` must be an instance of InterfaceSmsSenderAdapter, got `{}`"

    def __init__(self, adapter=None, number_list=None, content=None,
                 max_content_length=ValidateSmsContent.max_character_length):
        """     (class, list, string, int) -> instance

        :param {!instance} adapter: Sms sender adapter instance
        :param {!list} number_list: List of numbers to send sms content
        :param {!string} content: Sms content
        :param {?int} max_content_length: Maximum character length of `content`
        """
        self.max_content_length = max_content_length
        self.number_list = number_list
        self.content = content
        self.adapter = adapter

    def send_sms(self):
        self.adapter.number_list = self.number_list
        self.adapter.content = self.content
        result_dict, status_code = self.adapter.send_sms()
        return result_dict, status_code

    def get_log_data(self):
        return self.adapter.get_log_data()

    @property
    def adapter(self):
        return self.__adapter

    @adapter.setter
    def adapter(self, adapter):
        if not isinstance(adapter, InterfaceSmsSenderAdapter):
            raise ErrorTypeError(SmsSender.adapter_assert_error.format(type(adapter)))
        self.__adapter = adapter

    @property
    def number_list(self):
        return self.__number_list

    @number_list.setter
    def number_list(self, number_list):
        if isinstance(number_list, str):
            number_list = [number_list]
        self.__number_list = number_list

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, sms_content):
        self.__content = ValidateSmsContent(max_character=self.max_content_length).validate_content(sms_content)
