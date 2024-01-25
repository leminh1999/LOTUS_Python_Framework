import __init
from time import sleep
# import os
# os.environ['DISPLAY'] = '8702ba7a106e:1'
# os.environ['XAUTHORITY']='/root/.Xauthority'

from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# options = webdriver.ChromeOptions()
# service = ChromeService(executable_path='chromedriver.exe')
# driver = webdriver.Chrome(service=service)


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# chromeOptions = Options()
# chromeOptions.headless = False
# s = Service("/HShare/chromedriver")
# driver = webdriver.Chrome(service= s, options = chromeOptions )


print("1")
# options = webdriver.ChromeOptions()
# options.add_argument('disable-infobars')
# options.add_argument('--no-sandbox') # Bypass OS security model
# options.add_argument('start-maximized') #
# # options.add_argument("--disable-extensions")
# options.add_extension('Library/A3_Selenium/Components/Jubei_Captcha_Auth.zip')
# driver = webdriver.Remote(
#     command_executor='http://host.docker.internal:4444/wd/hub',
#     options=options
# )



options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
driver = webdriver.Chrome('chromedriver',options=options)
# driver = webdriver.Chrome(executable_path=r'chromedriver',options=options) #Linux chromedriver
driver.get("http://www.google.com")



print("2")
driver.get('https://python.org')
print("3")
driver.save_screenshot('screenshot.png')
print("5")

driver.quit()