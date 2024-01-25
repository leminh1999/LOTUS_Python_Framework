import __init
from Conf.loggingSetup import *
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from Library.A4_SendInBlue.Components.define import *
from enum import Enum

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = DEFAULT_API_KEY
api_mail_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
api_sms_instance  = sib_api_v3_sdk.TransactionalSMSApi(sib_api_v3_sdk.ApiClient(configuration))


class class_contentMode (Enum):
  PLAINTEXT_CONTENT = 1
  HTML_CONTENT      = 2

class mailConfig ():
  apiKey        = DEFAULT_API_KEY
  sender        = DEFAULT_SENDER
  to            = DEFAULT_TO
  cc            = DEFAULT_CC
  bcc           = DEFAULT_BCC
  reply_to      = DEFAULT_REPLY_TO
  subject       = DEFAULT_SUBJECT
  content_mode  = class_contentMode.PLAINTEXT_CONTENT
  html_content  = DEFAULT_HTML_CONT
  text_content  = DEFAULT_TEXT_CONT
  attachment    = DEFAULT_ATTACHMENT # list of file names (Cloud data)
  scheduled_at  = None #"2022-06-12T14:30:00+07:00" => Jun 12, 2022 at 14:30:00 GMT+07:00

class sendInBlue ():
  #################################################################
  def getAccountCredits (class_mailConfig):
    '''
    - `name`: getAccountCredits
    - `description`: Kiểm tra số dư tài khoản: email, sms
    - `parameters`: class_mailConfig
    - `return`: (emailCredits, smsCredits)
    - `Example`:
      - Step 1: defaultMailConf = mailConfig                               # create a mailConfig object
      - Step 2: mailCredit, smsCredit = getAccountCredits(defaultMailConf) # get the account credits
    - `PIC`:
      - ✨ ..\Components\PIC\Credits_Terminal.png
      - ✨ ..\Components\PIC\Credits_Web.png
    '''
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = class_mailConfig.apiKey
    api_instance = sib_api_v3_sdk.AccountApi(sib_api_v3_sdk.ApiClient(configuration))

    try:
        api_response = api_instance.get_account()
        # pprint(api_response)
        print("Email Credits: "+str(api_response.plan[0].credits))
        print("SMS Credits: "+str(api_response.plan[1].credits))
        return (api_response.plan[0].credits,api_response.plan[1].credits)
        
    except ApiException as e:
        print("Exception when calling AccountApi->get_account: %s\n" % e)
  
  
  #################################################################
  def sendMail (class_mailConfig):
    '''
    - `name`: sendMail
    - `description`: Send mail to a list of recipients -> PIC\mail.png
    - `parameters`: class_mailConfig
    - `return`: None
    - `Example`:
      - Step 1: defaultMailConf = mailConfig  # create a mailConfig object
      - Step 2: defaultMailConf.to = xxxx     # set the recipient and others parameters (if any).
      - Step 3: sendMail(defaultMailConf)     # send mail with the mailConfig object
    - `PIC`:
      - ✨ ..\Components\PIC\mail.png
    '''
    #1.Get all information
    sender = class_mailConfig.sender
    to = class_mailConfig.to
    cc = class_mailConfig.cc
    bcc = class_mailConfig.bcc
    reply_to = class_mailConfig.reply_to
    scheduled_at  = class_mailConfig.scheduled_at
    subject = class_mailConfig.subject
    content_mode = class_mailConfig.content_mode
    text_content = class_mailConfig.text_content
    html_content = class_mailConfig.html_content
    attachment = class_mailConfig.attachment
    headers = {"Some-Custom-Name":"unique-id-1234"}
    params = {"parameter":"My param value","subject":"New Subject"}
    
    #2. Add information to mail configuration
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
      sender=sender, 
      to = to, 
      cc = cc if cc else None, 
      bcc = bcc if bcc else None,
      reply_to= reply_to if reply_to else None,
      subject= subject,
      text_content = text_content if content_mode == class_contentMode.PLAINTEXT_CONTENT else None,
      html_content = html_content if content_mode == class_contentMode.HTML_CONTENT else None,
      scheduled_at = scheduled_at if scheduled_at else None,
      attachment   = attachment if len(attachment) != 0 else None,
      
      
      headers=headers,
      params=params,
    )
    #3. Send email
    try:
        api_response = api_mail_instance.send_transac_email(send_smtp_email)
        logger.info(api_response)
    except ApiException as e:
        logger.info("Exception when calling SMTP API->send_transac_email: %s\n" % e)

  #################################################################
  def sendVoiceCodeToPhone (phoneNum="84908549354", code="123456"):
    '''
    - `name`: sendVoiceCodeToPhone
    - `description`: Hệ thống tự động từ tổng đài sẽ gọi điện cho khách để đọc mac {code} -> PIC\call.jpg \\
                     Nếu người dùng không nghe máy, hệ thống sẽ gửi SMS cho khách kèm mã. -> PIC\sms.jpg \\
      `⛔CHÚ Ý`: Khi test thì thấy hệ thống không ổn định. Lúc gọi điện lúc không. Lúc có gửi SMS kèm mã, lúc không.
    - `parameters`:
      - `phoneNum`: phone number to send voice call
      - `code`: code to send to phone number
    - `return`: None
    - `Example`: sendInBlue.sendVoiceCodeToPhone(phoneNum="84908549354", code="123456")
    - `PIC`:
      - ✨ ..\Components\PIC\call.jpg
      - ✨ ..\Components\PIC\sms.jpg
    '''
    send_transac_sms = sib_api_v3_sdk.SendTransacSms(sender=phoneNum, recipient=phoneNum, content=code, type="transactional", web_url="https://example.com/notifyUrl")
    try:
        api_response = api_sms_instance.send_transac_sms(send_transac_sms)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TransactionalSMSApi->send_transac_sms: %s\n" % e)
    
#####################################
# defaultMailConf = mailConfig
# sendInBlue.sendMail(defaultMailConf)
# sendInBlue.sendVoiceCodeToPhone()
# sendInBlue.getAccountCredits(defaultMailConf)