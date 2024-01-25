import __init
from time import sleep
# import os
# os.environ['DISPLAY'] = '8702ba7a106e:1'
# os.environ['XAUTHORITY']='/root/.Xauthority'
from selenium import webdriver


print("1")
options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('start-maximized') #
# options.add_argument("--disable-extensions")
options.add_extension('Library/A3_Selenium/Components/Jubei_Captcha_Auth.zip')
driver = webdriver.Remote(
    command_executor='http://host.docker.internal:4444/wd/hub',
    options=options
)

print("2")
driver.get('https://python.org')
print("3")
driver.save_screenshot('screenshot.png')
print("5")
while True:
    sleep(1)
driver.quit()