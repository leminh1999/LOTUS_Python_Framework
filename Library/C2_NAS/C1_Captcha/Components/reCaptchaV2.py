from anticaptchaofficial.hcaptchaproxyless import * #Cài đặt trước thư viện: pip3 install anticaptchaofficial
from anticaptchaofficial.recaptchav2proxyless import *
from anticaptchaofficial.recaptchav3proxyless import *
from anticaptchaofficial.geetestproxyless import *
from Conf.loggingSetup import *

def captchaSolving (ANTICAPTCHA_KEY="59e566f10cedd483bd51b4b37f89f6b9",
              captchaType="hCaptcha",
              webUrl="https://democaptcha.com/demo-form-eng/hcaptcha.html",
              webKey="51829642-2cda-4b09-896c-594f89d700cc",
              gtKey="",
              challengeKey=""):
  '''
  - `name`: hCaptcha
  - `description`: Giải nhiều dạng captcha và output ra chuỗi response đùng để mở khóa.
  - `parameters`:
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
  if response != 0:
      return response
  else:
      logger.error("task finished with error "+solver.error_code)