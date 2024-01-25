import __init
from Library.A4_SendInBlue.Components.sendInBlue import mailConfig
from time import sleep
from pprint import pprint
from Conf.loggingSetup import *
from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB


SIB.sendVoiceCodeToPhone(phoneNum="84908549354", code="123456") #-> ../Components/PIC/call.jpg
                                                                #-> ../Components/PIC/sms.jpg


