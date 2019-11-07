# Short Url
Send text as SMS with adapters. For now only supports Callturk sender

```bash
pip install -i https://test.pypi.org/simple/ sms-service==0.0.3
```

## Supported Services
GoogleUrlShorter, BitLinkUrlShorter 
## Usage

```python
from sms_service import SmsSender, CallturkSmsSender
# ===> Usage with `CallturkSmsSender` adapter
callturk_adapter = CallturkSmsSender(
    username="callturk_user_name",
    password="callturk_user_password",
    organization_name="callturk_organization_name"
)
# Set SmsSender with callturk_adapter
sender = SmsSender(adapter=callturk_adapter,
                   content="YOUR SMS CONTENT HERE",
                   number_list=[5512223344, 9998885544])
# Now you can send sms
# if success it should return 201
response_dict, status_code = sender.send_sms()  # return -> tuple(dict, int)
# after sent sms you can get log data with;
print(sender.get_log_data())


```

## License
[MIT](https://choosealicense.com/licenses/mit/)
