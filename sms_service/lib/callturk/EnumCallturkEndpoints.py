from enum import Enum


class EnumCallturkEndpoint(Enum):
    WS = "https://sorgu.callturk.com.tr/cas/webservice"
    AUTH = "https://sorgu.callturk.com.tr/cas/webservice/authenticate/cas"
    SMS_SEND = "https://sorgu.callturk.com.tr/cas/webservice/secure/smssend"
    SMS_INFO = "https://sorgu.callturk.com.tr/cas/webservice/secure/smsinfo"
