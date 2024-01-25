# ✨ TRANG TẠO CAPTCHA ĐỂ TEST: https://democaptcha.com/

#pip3 install anticaptchaofficial

from anticaptchaofficial.hcaptchaproxyless import *

solver = hCaptchaProxyless()
solver.set_verbose(1)
solver.set_key("59e566f10cedd483bd51b4b37f89f6b9")
solver.set_website_url("https://democaptcha.com/demo-form-eng/hcaptcha.html")
solver.set_website_key("51829642-2cda-4b09-896c-594f89d700cc")

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

g_response = solver.solve_and_return_solution()
if g_response != 0:
    print ("g-response: "+g_response)
else:
    print ("task finished with error "+solver.error_code)

