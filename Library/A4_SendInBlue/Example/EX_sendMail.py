import __init
from Library.A4_SendInBlue.Components.sendInBlue import mailConfig
from time import sleep
from pprint import pprint
from Conf.loggingSetup import *
from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB

#Step 1: Create on object to send mail
mailConf_1 = mailConfig

#Step 2: Modify information if any
mailConf_1.to = [{"email":'tran.dung@cmengineering.com.vn',"name":"Tran Dung"}]
mailConf_1.subject = 'This is test mail'
mailConf_1.content_mode = class_contentMode.HTML_CONTENT

pprint(mailConf_1)
#Step 3: Send email
SIB.sendMail(mailConf_1) #-> ../Components/PIC/mail.png


