import __init
from time import sleep
from Conf.loggingSetup import *
from Library.C1_Captcha.captcha_Wrap import captcha_Wrapper as CAPTCHA
from pprint import *


result = CAPTCHA.hCaptcha("https://democaptcha.com/demo-form-eng/hcaptcha.html","51829642-2cda-4b09-896c-594f89d700cc")
pprint(result)

#RESULT:
# ../Components/PIC/hCaptcha_1.png
# ../Components/PIC/hCaptcha_2.png
# ../Components/PIC/hCaptcha_3.png
# ../Components/PIC/hCaptcha_4.png
