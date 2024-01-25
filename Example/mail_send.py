from __future__ import print_function
import time
import datetime
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

api_instance = sib_api_v3_sdk.EmailCampaignsApi(sib_api_v3_sdk.ApiClient(configuration))
campaign_id = 1
email_to = sib_api_v3_sdk.SendTestEmail(email_to=['tran.dung@cmengineering.com.vn', 'tranhuudung1986@gmail.com'])

try:
    api_instance.send_test_email(campaign_id, email_to)
except ApiException as e:
    print("Exception when calling EmailCampaignsApi->send_test_email: %s\n" % e)