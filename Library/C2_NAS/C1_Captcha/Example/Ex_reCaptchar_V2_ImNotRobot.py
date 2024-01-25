import __init
from time import sleep
from Conf.loggingSetup import *
from Library.C1_Captcha.captcha_Wrap import captcha_Wrapper as CAPTCHA
from pprint import *


result = CAPTCHA.reCaptchaV2("https://democaptcha.com/demo-form-eng/recaptcha-2.html","6LfGqN0UAAAAAFdGo4OSj5Awi8hM_9kmR7VfXUP2")
pprint(result)

#RESULT:
# ../Components/PIC/reCaptchaV2_1.png
# ../Components/PIC/reCaptchaV2_2.png
