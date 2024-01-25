from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

api_instance = sib_api_v3_sdk.TransactionalSMSApi(sib_api_v3_sdk.ApiClient(configuration))
send_transac_sms = sib_api_v3_sdk.SendTransacSms(sender="84909888580", recipient="84908549354", content="ABC", type="transactional", web_url="https://example.com/notifyUrl")

try:
    api_response = api_instance.send_transac_sms(send_transac_sms)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionalSMSApi->send_transac_sms: %s\n" % e)