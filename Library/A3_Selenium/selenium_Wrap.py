import __init
from Library.A3_Selenium.Components.SeleniumIDE import *

WEB = seleniumIDE()


#Import from Selenium IDE
class seleniumIDE_Remap ():
  class setup():
    begin = WEB.begin #CHÚ Ý: Nếu là being() thì sẽ thực thi hàm khi khởi tạo. Nếu chỉ muốn porting thì không gắn ().
    openWebForDebug = WEB.openWebForDebug #CHÚ Ý: Nếu là being() thì sẽ thực thi hàm khi khởi tạo. Nếu chỉ muốn porting thì không gắn ().
    quit = WEB.quit #CHÚ Ý: Nếu là being() thì sẽ thực thi hàm khi khởi tạo. Nếu chỉ muốn porting thì không gắn ().

  def printHello():
    print ("Hello from jubeiSeleniumIDERemap")

  class assertVerify ():
    '''Pic: Components/PIC/assertVerify.png'''
    assertTitle = WEB.assertTitle
    verifyTitle = WEB.verifyTitle
    assertVar = WEB.assertVar
    verifyVar = WEB.verifyVar
    assertValue = WEB.assertValue
    verifyValue = WEB.verifyValue
    assertText = WEB.assertText
    verifyText = WEB.verifyText
    assertNotText = WEB.assertNotText
    verifyNotText = WEB.verifyNotText
    assertSelectedLabel = WEB.assertSelectedLabel
    verifySelectedLabel = WEB.verifySelectedLabel
    assertSelectedValue = WEB.assertSelectedValue
    verifySelectedValue = WEB.verifySelectedValue
    assertNotSelectedValue = WEB.assertNotSelectedValue
    verifyNotSelectedValue = WEB.verifyNotSelectedValue
    assertChecked = WEB.assertChecked
    verifyChecked = WEB.verifyChecked
    assertNotChecked = WEB.assertNotChecked
    verifyNotChecked = WEB.verifyNotChecked
    assertEditable = WEB.assertEditable
    verifyEditable = WEB.verifyEditable
    assertNotEditable = WEB.assertNotEditable
    verifyNotEditable = WEB.verifyNotEditable
    assertElementPresent = WEB.assertElementPresent
    verifyElementPresent = WEB.verifyElementPresent
    assertElementNotPresent = WEB.assertElementNotPresent
    verifyElementNotPresent = WEB.verifyElementNotPresent
    assertAlert = WEB.assertAlert
    assertConfirmation = WEB.assertConfirmation
    assertPrompt = WEB.assertPrompt
    
  class waitFor ():
    '''Pic: Components/PIC/waitFor.png'''
    waitForElementPresent = WEB.waitForElementPresent
    waitForElementNotPresent = WEB.waitForElementNotPresent
    waitForElementVisible = WEB.waitForElementVisible
    waitForElementNotVisible = WEB.waitForElementNotVisible
    waitForElementEditable = WEB.waitForElementEditable
    waitForElementNotEditable = WEB.waitForElementNotEditable
    waitForText = WEB.waitForText
    waitForAttr = WEB.waitForAttr
    
  class mouseKey ():
    '''Pic: Components/PIC/mouseKey.png'''
    click = WEB.click
    doubleClick = WEB.doubleClick
    mouseDown = WEB.mouseDown
    mouseMove = WEB.mouseMove
    mouseUp = WEB.mouseUp
    dragAndDropToObject = WEB.dragAndDropToObject
    dragAndDropToObjectOffset = WEB.dragAndDropToObjectOffset
    mouseOver = WEB.mouseOver
    mouseOut = WEB.mouseOut
    type = WEB.type
    sendKeys = WEB.sendKeys
    
  class browser ():
    '''Pic: Components/PIC/browser.png'''
    open = WEB.open
    setWindowSize = WEB.setWindowSize
    selectWindow = WEB.selectWindow
    close = WEB.close
    pause = WEB.pause
    echo = WEB.echo
    runScript = WEB.runScript
    executeScript = WEB.executeScript
    executeAsyncScript = WEB.executeAsyncScript

  class store ():
    '''Pic: Components/PIC/store.png'''
    storeTitle = WEB.storeTitle
    store = WEB.store
    storeValue = WEB.storeValue
    storeText = WEB.storeText
    storeAttribute = WEB.storeAttribute
    storeXpathCount = WEB.storeXpathCount
    storeJson = WEB.storeJson
    storeWindowHandler = WEB.storeWindowHandler
    
  class webContent ():
    '''Pic: Components/PIC/webContent.png'''
    select = WEB.select
    check = WEB.check
    unCheck = WEB.unCheck
    editContent = WEB.editContent
    addSelection = WEB.addSelection
    removeSelection = WEB.removeSelection
    selectFrame = WEB.selectFrame
    webdriverChooseOkOnVisibleConfirmation = WEB.webdriverChooseOkOnVisibleConfirmation
    webdriverChooseCancelVisibleConfirmation = WEB.webdriverChooseCancelVisibleConfirmation
    webdriverAnswerOnVisiblePrompt = WEB.webdriverAnswerOnVisiblePrompt
    webdriverChooseCancelOnVisiblePrompt = WEB.webdriverChooseCancelOnVisiblePrompt

  class others ():
    others_content_findFirstElement = WEB.others_content_findFirstElement
    others_content_findAllElements = WEB.others_content_findAllElements
    others_content_findLastElement = WEB.others_content_findLastElement
    others_browser_getCurrentURL = WEB.others_browser_getCurrentURL
    others_content_getPageSourceCode = WEB.others_content_getPageSourceCode
    others_browser_closeCurrentTab = WEB.others_browser_closeCurrentTab
    others_browser_closeAllRightTabs = WEB.others_browser_closeAllRightTabs
    others_browser_closeAllOtherTabs = WEB.others_browser_closeAllOtherTabs
    others_browser_getNumberOfTabs = WEB.others_browser_getNumberOfTabs
    others_browser_maximizeWindow = WEB.others_browser_maximizeWindow
    others_browser_minimizeWindow = WEB.others_browser_minimizeWindow
    others_browser_fullscreenWindow = WEB.others_browser_fullscreenWindow
    others_browser_printPagePDF = WEB.others_browser_printPagePDF
    others_browser_navigationBack = WEB.others_browser_navigationBack
    others_browser_navigationFoward = WEB.others_browser_navigationFoward
    others_browser_navigationRefresh = WEB.others_browser_navigationRefresh
    others_browser_setPageLoadTimeout = WEB.others_browser_setPageLoadTimeout
    others_browser_saveCurrentScreenshot = WEB.others_browser_saveCurrentScreenshot
    others_browser_getWindowSize = WEB.others_browser_getWindowSize
    others_browser_getBrowserPosition = WEB.others_browser_getBrowserPosition
    others_browser_setBrowserPosition = WEB.others_browser_setBrowserPosition
    others_browser_waitCaptchaSolving = WEB.others_browser_waitCaptchaSolving
    others_keyMouse_rightClick = WEB.others_keyMouse_rightClick
    others_keyMouse_hotkeys = WEB.others_keyMouse_hotkeys
    others_content_getNumberOfIframes = WEB.others_content_getNumberOfIframes
    others_content_waitNewIframeOpen = WEB.others_content_waitNewIframeOpen
    others_content_getAttribute = WEB.others_content_getAttribute
    others_content_getText = WEB.others_content_getText
    others_debug_printTabIframeInfo = WEB.others_debug_printTabIframeInfo
    others_browser_scrollTo = WEB.others_browser_scrollTo
    others_browser_scrollToElement = WEB.others_browser_scrollToElement
    others_browser_findChildElement = WEB.others_browser_findChildElement
    others_browser_findChildElements = WEB.others_browser_findChildElements
    others_print_comment_only = WEB.others_debug_printComment
    others_refreshBrowserTabNumOnly = WEB.refreshBrowserTabNumOnly
    others_refreshBrowserTabInfo = WEB.refreshBrowserTabInfo
    others_clearReqWaitCmdFlg = WEB.clearReqWaitCmdFlg
    others_clearExitOnExceptionFlg = WEB.clearExitOnExceptionFlg
    others_setExitOnExceptionFlg = WEB.setExitOnExceptionFlg
    others_content_getPosSizeElement = WEB.others_content_getPosSizeElement
    others_content_getPosMidElement = WEB.others_content_getPosMidElement
    others_content_saveElementScreenshot = WEB.others_content_saveElementScreenshot
    
    
  class getter():
    def getDefaultWaitTimeMs ():
      '''Default timeout of Wait For commands in ms'''
      return WEB.defaultWaitTimeMs 
    
    def getVars ():
      '''Dictionary of variables'''
      return WEB.vars
    
    def getPrintOutEna ():
      '''Print out enable'''
      return WEB.printOutEna
    
    def getPrintOutLevel():
      '''8 levels: Fatal/Error/Warn/Info/Debug/Trace/Terminal/NoPrint'''
      return WEB.printOutLevel
    
    def getCommandNum():
      '''Counter of Selenium commands'''
      return WEB.commandNum
    
    def getBrowserTabList():
      '''List of browser tab name. Call `refreshBrowserTabInfo` to update.'''
      return WEB.browserTabList
    
    def getBrowserTabHandle():
      '''List of browser tab handle. Call `refreshBrowserTabInfo` to update.'''
      return WEB.browserTabHandle
    
    def getBrowserTabNum():
      '''List of browser tab number. Call `refreshBrowserTabInfo` to update.'''
      return WEB.browserTabNum
  
  
  class setter():
    def setDefaultWaitTimeMs (defaultWaitTimeMs):
      '''Default timeout of Wait For commands in ms'''
      WEB.defaultWaitTimeMs = defaultWaitTimeMs
    
    def setVars (key, value):
      '''Dictionary of variables'''
      WEB.vars[key] = value
    
    def setPrintOutEna (trueFalse):
      '''Print out enable'''
      WEB.printOutEna = trueFalse
    
    def setPrintOutLevel(levels):
      '''8 levels: Fatal/Error/Warn/Info/Debug/Trace/Terminal/NoPrint'''
      WEB.printOutLevel = levels
    
    def setCommandNum(commandNumber):
      '''Counter of Selenium commands'''
      WEB.commandNum = commandNumber
    
    def setBrowserTabList(newTabList):
      '''List of browser tab name. Call `refreshBrowserTabInfo` to update.'''
      WEB.browserTabList = newTabList
    
    def setBrowserTabHandle(newTabHandleList):
      '''List of browser tab handle. Call `refreshBrowserTabInfo` to update.'''
      WEB.browserTabHandle = newTabHandleList
    
    def setBrowserTabNum(tabNum):
      '''List of browser tab number. Call `refreshBrowserTabInfo` to update.'''
      WEB.browserTabNum = tabNum


