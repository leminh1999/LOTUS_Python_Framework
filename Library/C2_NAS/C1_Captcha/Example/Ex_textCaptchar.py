import __init
from time import sleep
from Conf.loggingSetup import *
from Library.C1_Captcha.captcha_Wrap import captcha_Wrapper as CAPTCHA
from pprint import *


result = CAPTCHA.textCaptcha("Library/C1_Captcha/Components/PIC/textCaptcha_1.png")
pprint(result)

#RESULT:
# ../Components/PIC/textCaptcha_1.png
# ../Components/PIC/textCaptcha_2.png
