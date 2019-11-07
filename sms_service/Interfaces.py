#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class InterfaceSmsContent(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate_content(self, content_string):
        """
        Check string is valid for sms
        :param {!str} content_string: Sms text content
        :return: {str}
        :raise: {Errors.ErrorValidationSmsContent}
        """
        pass


class InterfaceSetSmsAdapter(object):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def adapter(self):
        pass

    @adapter.setter
    @abstractmethod
    def adapter(self, value):
        pass


class InterfaceSmsSender(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_sms(self):
        pass

    @property
    @abstractmethod
    def number_list(self):
        pass

    @number_list.setter
    @abstractmethod
    def number_list(self, number_list):
        pass

    @property
    @abstractmethod
    def content(self):
        pass

    @content.setter
    @abstractmethod
    def content(self, sms_content):
        pass


class InterfaceSmsSenderAdapter(InterfaceSmsSender):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_log_data(self):
        """Should return dict as;
        data=dict(
            content=str
            number_list=list
            request_body={ANY}
        )
        :return dict(
            data=data,
            response=dict,
            status_code=int
            url=string
            method=string
        )
        """
        pass

    @abstractmethod
    def handle_sms_response(self, response):
        """
        `self.send_sms` response handler
        :param {Any} response:
        :return: {tuple}: (dict, int)
        if its successful then:
            `dict` value will contains `id` key
            and `int` value will equals `201`
        else:
            `dict` will be descripted in `handle_sms_error_response` check it out,
            and `int` value will be greater than 201
        """
        pass

    @abstractmethod
    def handle_sms_error_response(self, response):
        """
        If `self.send_sms` returned with errors then prepare a standard error dict
        :param {Any} response:
        :return: dict(
            message='ERROR_MESSAGE_TITLE'
            description='ERROR_MESSAGE_DESCRIPTION'
            errors=[{},{}],
            status_code=400 # response.status_code
        )
        """
        pass


class InterfaceXmlController(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_as_string(self):
        """
        :return: xml string
        """
        pass

    @property
    @abstractmethod
    def xml(self):
        pass

    @xml.setter
    @abstractmethod
    def xml(self, value):
        pass
