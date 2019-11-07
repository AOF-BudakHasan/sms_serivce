#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .Interfaces import InterfaceSmsContent
from .Errors import SmsContentTypeError, SmsContentLengthError


class ValidateSmsContent(InterfaceSmsContent):
    """
    Validate Sms content text
    """
    instance_error = "Parameter `content_string` should be `<class 'str'>` not {}"
    length_error = "Too long ({content} character). Content string should be lower than {max_character} character"
    max_character_length = 700

    def __init__(self, max_character=max_character_length):
        self.max_character = max_character

    def validate_content(self, content_string):
        """
        Check sms text raise Exceptions if it is not valid
        :param {str} content_string: Sms content string
        :return: str
        :raises {ErrorValidationSmsContent}:
            :SmsContentTypeError: Raise if `content_string` type is not <class 'str'>
            :SmsContentLengthError: Raise if content length higher than `max_character_length`
        """
        if not isinstance(content_string, str):
            raise SmsContentTypeError(ValidateSmsContent.instance_error.format(type(content_string)))
        if len(content_string) >= self.max_character:
            raise SmsContentLengthError(ValidateSmsContent.length_error
                                        .format(content=len(content_string),
                                                max_character=self.max_character))
        return content_string
