#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ErrorServiceTopLevelException(Exception):
    pass


class ErrorValidationSmsContent(ErrorServiceTopLevelException):
    pass


class SmsContentTypeError(ErrorValidationSmsContent):
    pass


class SmsContentLengthError(ErrorValidationSmsContent):
    pass


class ErrorSmsSender(ErrorServiceTopLevelException):
    pass


class ErrorTypeError(ErrorServiceTopLevelException):
    pass


class ErrorWebServiceError(ErrorServiceTopLevelException):
    pass


class ErrorTokenExpired(ErrorServiceTopLevelException):
    pass
