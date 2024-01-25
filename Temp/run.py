from myApp import *
from urllib.parse import unquote
app = myApp()


def makeListOfVideoLinkTask1 ():
  for clip in app.elements:
    # app.chrome.others_browser_scrollToElement(clip)
    app.chrome.runScript(("window.scrollTo(0,"+str(clip.location['y'])+")"))
    delay(1000)
    shareIconLoc = clip.find_element(By.XPATH,"./child::*//span[@data-e2e='share-icon']/parent::button")
    # print(shareIconLoc.location['x'])
    # print(shareIconLoc.location['y'])
    
    actions = ActionChains(app.chrome.driver)
    actions.move_to_element(shareIconLoc).perform()
    app.chrome.waitForElementPresent("xpath=//a[@data-e2e='video-share-whatsapp']")
    videoLink = app.chrome.findElement("xpath=//a[@data-e2e='video-share-whatsapp']").get_attribute('href')
    videoLink = unquote(videoLink).split("text=")[1]
    print(videoLink)
    






app.openChrome()
# app.loginAccount()
app.scrollClipPost()
app.checkClipPostCondition()
print(app.task1ConditionPassedList)
makeListOfVideoLinkTask1()






delay(5000000)
