import os

callturk_dir = os.path.join('sms_service', 'lib', 'callturk', 'xml', '{}', '{}')


def mocked_callturk_auth_failed(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def text(self):
            return self.text
    xml_path = callturk_dir.format('authentication', 'authenticate.response.failed.xml')
    with open(xml_path, 'r', encoding="utf8") as response_xml:
        xml = response_xml.read().replace('\n', '').replace('  ', '')
    return MockResponse(xml, 200)


def mocked_callturk_auth_success(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def text(self):
            return self.text
    xml_path = callturk_dir.format('authentication', 'authenticate.response.success.xml')
    with open(xml_path, 'r', encoding="utf8") as response_xml:
        xml = response_xml.read().replace('\n', '').replace('  ', '')
    return MockResponse(xml, 200)


def mocked_callturk_sms_send_failed(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def text(self):
            return self.text

    xml_path = callturk_dir.format('sms_send', 'sms_send.response.failed.xml')
    with open(xml_path, 'r', encoding="utf8") as response_xml:
        xml = response_xml.read().replace('\n', '').replace('  ', '')
    return MockResponse(xml, 200)


def mocked_callturk_sms_send_success(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def text(self):
            return self.text

    xml_path = callturk_dir.format('sms_send', 'sms_send.response.success.xml')
    with open(xml_path, 'r', encoding="utf8") as response_xml:
        xml = response_xml.read().replace('\n', '').replace('  ', '')
    return MockResponse(xml, 200)


def mocked_callturk_session_expired(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def text(self):
            return self.text

    xml_path = callturk_dir.format('sms_send', 'sms_send.response.failed.xml')
    with open(xml_path, 'r', encoding="utf8") as response_xml:
        xml = response_xml.read().replace('\n', '').replace('  ', '')
    return MockResponse(xml, 401)
