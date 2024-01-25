import __init
from Library.C3_OmoCaptcha.omoCaptcha import omoCaptcha

OMO = omoCaptcha()

################################
### 1. Giải Captcha from URL ###
################################
print(OMO.getBalance())
insideImg  = "https://p16-captcha-va.ibyteimg.com/tos-maliva-i-71rtze2081-us/03b27b7271dd468395b63fce04305c94~tplv-71rtze2081-1.png"
outsideImg = "https://p16-captcha-va.ibyteimg.com/tos-maliva-i-71rtze2081-us/3edac5dd33654402b1d249f9c3caed11~tplv-71rtze2081-1.png"
print(OMO.solveTiktokRotateImage(imageInsidePathOrUrl=insideImg,imageOutsidePathOrUrl=outsideImg))
print(OMO.getBalance())
#### RESULT => Library/C3_OmoCaptcha/Components/PIC/result_choose2Samecaptcha.png ####
# (True, '0.98020')          -> Tài khoản ban đầu có 0.98020$
# (True, '117')              -> Giải captcha thành công. Kéo slide để xoay hình 117 độ.
# (True, '0.97960')          -> Tài khoản sau khi giải captcha còn 0.97960$



##############################################
### 2. Giải Captcha từ hình có sẵn ở Local ###
##############################################
print(OMO.getBalance())
insideImg  = "Library/C3_OmoCaptcha/Components/PIC/tiktokRotateInside.png"
outsideImg = "Library/C3_OmoCaptcha/Components/PIC/tiktokRotateOutside.png"
print(OMO.solveTiktokRotateImage(imageInsidePathOrUrl=insideImg,imageOutsidePathOrUrl=outsideImg))
print(OMO.getBalance())
#### RESULT => Library/C3_OmoCaptcha/Components/PIC/result_choose2Samecaptcha.png ####
# (True, '0.98020')          -> Tài khoản ban đầu có 0.98020$
# (True, '57')               -> Giải captcha thành công. Kéo slide để xoay hình 57 độ.
# (True, '0.97960')          -> Tài khoản sau khi giải captcha còn 0.97960$