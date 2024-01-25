import __init
from Library.A4_SendInBlue.Components.sendInBlue import mailConfig
from Conf.loggingSetup import *
from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB


defaultMailConf = mailConfig
SIB.getAccountCredits(defaultMailConf)

# ../Components/PIC/Credits_Terminal.png
# ../Components/PIC/Credits_Web.png


