import __init
# import os
# os.environ['DISPLAY'] = '8702ba7a106e:1'
# os.environ['XAUTHORITY']='/root/.Xauthority'
# os.system("echo $DISPLAY")
# os.system("echo $XAUTHORITY")

# from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A3_Selenium.selenium_Wrap import WEB, seleniumIDE_Remap as IDE

IDE.setup.begin("Chrome",headless=False)
IDE.browser.open("https://www.google.com/")

IDE.mouseKey.click('name=q')
# IDE.mouseKey.type('name=q', 'NAMO AMITABHA BUDDHA')
WEB.driver.find_element_by_name('q').send_keys('NAMO AMITABHA BUDDHA')

IDE.mouseKey.sendKeys("name=q","${KEY_ENTER}",'Print Hello World')
IDE.others.others_browser_scrollTo('0','2000')
IDE.others.others_print_comment_only('Hello World1', 'Hello World2', 'Hello World3')

IDE.others.others_debug_printTabIframeInfo()

print(WEB.driver.page_source)

IDE.setup.quit()
print("===== END =====")