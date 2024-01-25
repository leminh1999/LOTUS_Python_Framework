import __init
from Library.C3_OmoCaptcha.omoCaptcha import omoCaptcha

OMO = omoCaptcha()
print(OMO.getBalance())
print(OMO.solveTiktokChoose2Same("Library/C3_OmoCaptcha/Components/PIC/choose2Samecaptcha.png"))
print(OMO.getBalance())

#### RESULT => Library/C3_OmoCaptcha/Components/PIC/result_choose2Samecaptcha.png ####
# (True, '0.98020')          -> Tài khoản ban đầu có 0.98020$
# (True, '239|57|83|186')    -> Giải captcha thành công. Vị trí: (x1,y1) = (239,57). (x2,y2) = (83,186)
# (True, '0.97960')          -> Tài khoản sau khi giải captcha còn 0.97960$

