import __init
from Conf.loggingSetup import *

#pip3 install anticaptchaofficial
#pip3 install python3_anticaptcha
from python3_anticaptcha import ImageToTextTask
from anticaptchaofficial.hcaptchaproxyless import * #Cài đặt trước thư viện: pip3 install anticaptchaofficial
from anticaptchaofficial.recaptchav2proxyless import *
from anticaptchaofficial.recaptchav3proxyless import *
from anticaptchaofficial.geetestproxyless import *

# ✨ TRANG TẠO CAPTCHA ĐỂ TEST: https://democaptcha.com/

# Tài khoản giải CAPTCHA
# https://anti-captcha.com/
# account: meomay22
ANTICAPTCHA_KEY="59e566f10cedd483bd51b4b37f89f6b9" 

class CaptchaType:
  IMAGECAPTCHA  = "imageCaptcha"
  HCAPTCHAR     = "hCaptcha"
  RECAPTCHAR_V2 = "reCaptchaV2"
  RECAPTCHAR_V3 = "reCaptchaV3"
  GEECAPTCHAR   = "geeTestCaptcha"


class captcha_Wrapper():
  def textCaptcha (filepath_or_url="Components/PIC/textCaptcha_1.png"):
    '''
    - `name`: textCaptcha (Cost: 0.0007$/time)
    - `description`: Giải captcha text và output ra chuỗi text (nằm trong dictionary).
    - `parameters`:
      - `filepath_or_url`: nhập vào URL của anh cần giải hoặc đường dẫn đến file ảnh cần giải.
    - `return`: chuỗi text (nằm trong dictionary). Components/PIC/textCaptcha_2.png
    - `Example`:
      - `textCaptcha("Components/PIC/textCaptcha_1.png")`
    - `PIC`: ✨ Components/PIC/textCaptcha_2.png
    '''
    try:
      if "http" in filepath_or_url:
        user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = ANTICAPTCHA_KEY).captcha_handler(captcha_link=filepath_or_url)
      else:
        user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = ANTICAPTCHA_KEY).captcha_handler(captcha_file=filepath_or_url)
      return user_answer
    except:
      logger.error("Error: textCaptcha cannot gernate")

  def hCaptcha (webUrl="https://democaptcha.com/demo-form-eng/hcaptcha.html",webKey="51829642-2cda-4b09-896c-594f89d700cc"):
    '''
    - `name`: hCaptcha (Cost: 0.002$/time)
    - `description`: Giải hcaptcha và output ra chuỗi response đùng để mở khóa hCaptcha.
    - `parameters`:
      - `webUrl`: đường dẫn đến trang web cần giải hcaptcha.
      - `webKey`: key của web tích hợp bảo mật hcaptcha. Các tra key: Components/PIC/hCaptcha_2.png
    - `return`: chuỗi response đùng để mở khóa hCaptcha. Components/PIC/hCaptcha_3.png
    - `Example`:
      - hCaptcha("https://democaptcha.com/demo-form-eng/hcaptcha.html","51829642-2cda-4b09-896c-594f89d700cc")
    - PIC: ✨ Components/PIC/hCaptcha_1.png
    - PIC: ✨ Components/PIC/hCaptcha_2.png
    - PIC: ✨ Components/PIC/hCaptcha_3.png
    - PIC: ✨ Components/PIC/hCaptcha_4.png
    '''
    return captcha_Wrapper.__captchaSolving(CaptchaType.HCAPTCHAR, webUrl,webKey)

  def reCaptchaV2 (webUrl="https://democaptcha.com/demo-form-eng/hcaptcha.html",webKey="51829642-2cda-4b09-896c-594f89d700cc"):
    '''
    - `name`: reCaptchaV2 (Cost: 0.002$/time)
    - `description`: Giải reCaptchaV2 và output ra chuỗi response đùng để mở khóa reCaptchaV2.
    - `parameters`:
      - `webUrl`: đường dẫn đến trang web cần giải reCaptchaV2.
      - `webKey`: key của web tích hợp bảo mật reCaptchaV2. Các tra key: Components/PIC/hCaptcha_2.png
    - `return`: chuỗi response đùng để mở khóa hCaptcha. Components/PIC/hCaptcha_3.png
    '''
    return captcha_Wrapper.__captchaSolving(CaptchaType.RECAPTCHAR_V2, webUrl,webKey)

  def reCaptchaV3 (webUrl="https://democaptcha.com/demo-form-eng/hcaptcha.html",webKey="51829642-2cda-4b09-896c-594f89d700cc"):
    '''
    - `name`: reCaptchaV3
    - `description`: Giải reCaptchaV3 và output ra chuỗi response đùng để mở khóa reCaptchaV3.
    - `parameters`:
      - `webUrl`: đường dẫn đến trang web cần giải reCaptchaV3.
      - `webKey`: key của web tích hợp bảo mật reCaptchaV3. Các tra key: Components/PIC/hCaptcha_2.png
    - `return`: chuỗi response đùng để mở khóa hCaptcha. Components/PIC/hCaptcha_3.png
    '''
    return captcha_Wrapper.__captchaSolving(CaptchaType.RECAPTCHAR_V3, webUrl,webKey)
        
  def geeTestCaptcha (webUrl="https://democaptcha.com/demo-form-eng/hcaptcha.html",gtKey="",challengeKey=""):
    '''
    - `name`: geeTestCaptcha
    - `description`: Giải geeTestCaptcha và output ra chuỗi response đùng để mở khóa geeTestCaptcha.
    - `parameters`:
      - `webUrl`: đường dẫn đến trang web cần giải geeTestCaptcha.
      - `gtKey`: Update later ???
      - `challengeKey`: Update later ???
    - `return`: chuỗi response đùng để mở khóa geeTestCaptcha.
    '''
    return captcha_Wrapper.__captchaSolving(CaptchaType.RECAPTCHAR_V3, webUrl,"",gtKey,challengeKey)
    
  def antiGateCaptcha ():
    '''
    Will be define later: https://anti-captcha.com/vi/apidoc/articles/how-to-bypass-any-captcha \n
    Will be define later: https://anti-captcha.com/vi/apidoc/articles/how-to-integrate-the-plugin
    '''
    print("Will be define later: https://anti-captcha.com/vi/apidoc/articles/how-to-bypass-any-captcha")
    print("Will be define later: https://anti-captcha.com/vi/apidoc/articles/how-to-integrate-the-plugin")
    
  #####################################################################################
  def __captchaSolving (captchaType="hCaptcha",
                webUrl="https://democaptcha.com/demo-form-eng/hcaptcha.html",
                webKey="51829642-2cda-4b09-896c-594f89d700cc",
                gtKey="",
                challengeKey=""):
    '''
    - `name`: hCaptcha
    - `description`: Giải nhiều dạng captcha và output ra chuỗi response đùng để mở khóa.
    - `parameters`:
      - `captchaType`: loại captcha cần giải. Gồm: hCaptcha,reCaptchaV2,reCaptchaV3,geeTestCaptcha.
      - `webUrl`: đường dẫn đến trang web cần giải hcaptcha.
      - `webKey`: key của web tích hợp bảo mật hcaptcha. Các tra key: Components/PIC/hCaptcha_2.png
      - `gtKey`: key dùng riêng cho loại captcha geetest.
      - `challengeKey`: key dùng riêng cho loại captcha geetest.
    - `return`: chuỗi response đùng để mở khóa captcha.
    '''
    if captchaType == "hCaptcha": 
      solver = hCaptchaProxyless()
      solver.set_verbose(1)
      solver.set_key(ANTICAPTCHA_KEY)
      solver.set_website_url(webUrl)
      solver.set_website_key(webKey)  #Xác định webKey: Components/PIC/hCaptcha_2.png (data-sitekey)
      
    if captchaType == "reCaptchaV2":
      solver = recaptchaV2Proxyless()
      solver.set_verbose(1)
      solver.set_key(ANTICAPTCHA_KEY)
      solver.set_website_url(webUrl)
      solver.set_website_key(webKey)  #Xác định webKey: Components/PIC/hCaptcha_2.png (data-sitekey)
      
    if captchaType == "reCaptchaV3":
      solver = recaptchaV3Proxyless()
      solver.set_verbose(1)
      solver.set_key(ANTICAPTCHA_KEY)
      solver.set_website_url(webUrl)
      solver.set_website_key(webKey)  #Xác định webKey: Components/PIC/hCaptcha_2.png (data-sitekey)
      solver.set_page_action("home_page")
      solver.set_min_score(0.9)
    
    if captchaType == "geeTestCaptcha":
      solver = geetestProxyless()
      solver.set_verbose(1)
      solver.set_key(ANTICAPTCHA_KEY)
      solver.set_website_url(webUrl)
      solver.set_gt_key("CONSTANT_GT_KEY")
      solver.set_challenge_key("VARIABLE_CHALLENGE_KEY")
    
    # tell API that Hcaptcha is invisible
    #solver.set_is_invisible(1)

    # set here parameters like rqdata, sentry, apiEndpoint, endpoint, reportapi, assethost, imghost
    #solver.set_enterprise_payload({
    #    "rqdata": "rq data value from target website",
    #    "sentry": True
    #})

    # Specify softId to earn 10% commission with your app.
    # Get your softId here: https://anti-captcha.com/clients/tools/devcenter
    solver.set_soft_id(0)

    response = solver.solve_and_return_solution()
    # print("DONE")
    # print("Response: " + str(response))
    if response != 0:
        return str(response)
    else:
        logger.error("task finished with error "+solver.error_code)