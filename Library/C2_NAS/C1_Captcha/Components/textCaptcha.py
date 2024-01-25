import __init

from python3_anticaptcha import ImageToTextTask
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = "59e566f10cedd483bd51b4b37f89f6b9"

# #1. Captcha Image from a link 
# Link to captcha image.
# image_link = "https://pythoncaptcha.tech/static/image/common_image_example/800070.png"
# Get string for solve captcha, and some other info.
# user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = ANTICAPTCHA_KEY).captcha_handler(captcha_link=image_link)

# #1. Captcha Image from a local file 
user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = ANTICAPTCHA_KEY).captcha_handler(captcha_file="Captcha_Text_Image.png")

print(user_answer)
