import os
import io
import unittest
from unittest.mock import patch

from sms_service import Errors, Interfaces
from sms_service import SmsSender
from sms_service.ValidateSmsContent import ValidateSmsContent
from sms_service.lib.callturk.CallturkSmsSender import CallturkSmsSender
from sms_service.lib.callturk.xml.sms_send.SmsSendController import SmsSendXmlController
from sms_service.lib.callturk.xml.authentication.AuthenticationXmlController import AuthenticationXmlController
from sms_service.tests.mocks.sms_sender__mock import (
    mocked_callturk_auth_failed,
    mocked_callturk_auth_success,
    mocked_callturk_sms_send_success,
    mocked_callturk_sms_send_failed,
    mocked_callturk_session_expired
)


class SmsSenderTests(unittest.TestCase):
    """
    SmsSender sınıf testleri
    """
    user_email = 'budak.hasan.apc@gmail.com'
    user_pass = 'TestPassword'
    callturk_user_name = 'TestUserName'
    callturk_user_pass = 'TestUserPassword'
    callturk_organization_name = 'TestOrganizationName'
    cache_token_key = "{}-{}".format(callturk_user_name, callturk_organization_name)
    valid_number_list = ['5551112233', '5552221133']
    valid_sms_content = 'Some Sms Content'

    def setUp(self):
        pass

    @patch('requests.post', side_effect=mocked_callturk_auth_failed)
    def test_callturk_auth_class_failed(self, mock_post):
        auth_ctrl = AuthenticationXmlController(
            username=SmsSenderTests.callturk_user_name,
            password=SmsSenderTests.callturk_user_pass,
            organization_name=SmsSenderTests.callturk_organization_name
        )
        self.assertIsInstance(auth_ctrl, Interfaces.InterfaceXmlController)
        # "ErrorWebServiceError should be raises if callturk credentials are wrong"
        self.assertRaises(Errors.ErrorWebServiceError, auth_ctrl.get_auth_token)

    @patch('requests.post', side_effect=mocked_callturk_auth_success)
    def test_callturk_auth_class_success(self, mock_post):
        auth_ctrl = AuthenticationXmlController(
            username=SmsSenderTests.callturk_user_name,
            password=SmsSenderTests.callturk_user_pass,
            organization_name=SmsSenderTests.callturk_organization_name
        )
        self.assertIsInstance(auth_ctrl, Interfaces.InterfaceXmlController)
        auth_token = auth_ctrl.get_auth_token()
        self.assertIsInstance(auth_token, str, "Request should return token value as str")

    @patch('requests.post', side_effect=mocked_callturk_session_expired)
    def test_callturk_sms_send_class_session_expired(self, mock_post):
        sms_send_ctrl = SmsSendXmlController(
            auth_token='SomeAuthToken',
            sms_content=SmsSenderTests.valid_sms_content,
            number_list=SmsSenderTests.valid_number_list,
        )
        self.assertIsInstance(sms_send_ctrl, Interfaces.InterfaceXmlController)
        # "ErrorTokenExpired should be raises if auth_token is expired"
        self.assertRaises(Errors.ErrorTokenExpired, sms_send_ctrl.send_sms)

    @patch('requests.post', side_effect=mocked_callturk_sms_send_failed)
    def test_callturk_sms_send_class_failed(self, mock_post):
        sms_send_ctrl = SmsSendXmlController(
            auth_token='SomeAuthToken',
            sms_content=SmsSenderTests.valid_sms_content,
            number_list=SmsSenderTests.valid_number_list,
        )
        self.assertIsInstance(sms_send_ctrl, Interfaces.InterfaceXmlController)
        # "ErrorWebServiceError should be raises if callturk credentials are wrong"
        self.assertRaises(Errors.ErrorWebServiceError, sms_send_ctrl.send_sms)

    @patch('requests.post', side_effect=mocked_callturk_sms_send_success)
    def test_callturk_sms_send_class_success(self, mock_post):
        sms_send_ctrl = SmsSendXmlController(
            auth_token='SomeAuthToken',
            sms_content=SmsSenderTests.valid_sms_content,
            number_list=SmsSenderTests.valid_number_list,
        )
        self.assertIsInstance(sms_send_ctrl, Interfaces.InterfaceXmlController)
        sms_send_request_id = sms_send_ctrl.send_sms()
        self.assertIsInstance(sms_send_request_id, str, "Request should return smsSendRequestId value as str")

    @patch('requests.post', side_effect=mocked_callturk_sms_send_success)
    def test_sms_sender_with_callturk_adapter(self, mock_post):
        callturk_adapter = CallturkSmsSender(
            username=SmsSenderTests.callturk_user_name,
            password=SmsSenderTests.callturk_user_pass,
            organization_name=SmsSenderTests.callturk_organization_name
        )
        CallturkSmsSender.REGISTERED_TOKENS[callturk_adapter.registered_token_key] = 'SomeAuthToken'
        # Set SmsSender with callturk_adapter
        sender = SmsSender(adapter=callturk_adapter,
                           content=SmsSenderTests.valid_sms_content,
                           number_list=SmsSenderTests.valid_number_list)
        # Test invalid content with `SmsContentTypeError`
        with self.assertRaises(Errors.SmsContentTypeError):
            sender.content = 1122313
        # Test invalid content as too long as expected `SmsContentLengthError`
        with self.assertRaises(Errors.SmsContentLengthError):
            too_long_content = ''
            for _ in range(ValidateSmsContent.max_character_length + 1):
                too_long_content += 'a'
            sender.content = too_long_content
            del too_long_content
        sender.content = SmsSenderTests.valid_sms_content

        response_dict, status_code = sender.send_sms()
        self.assertEqual(status_code, 201, 'Status code should be 201 if success')
        self.assertIsInstance(response_dict, dict, 'SmsSender.sms_send method should return dict in tuple as first')
        self.assertTrue('id' in response_dict, 'Response_dict should contain the id key')
        self.assertIsInstance(response_dict['id'], str, 'The id\'s value should be a string')
        log_data = sender.get_log_data()
        self.assertIsInstance(log_data, dict, '`get_log_data` function should return a dict')
        print(log_data)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
