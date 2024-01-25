import __init
import pyautogui
from Library.A2_LOTUS.lotus_Wrap import rgb,lotus_Remap as LOTUS

WINDOW = False #True if run in window, False if run in Linux

# ORG = pyautogui
class pyAutoGui_Remap ():
  '''Tham khảo hàm: https://pyautogui.readthedocs.io/en/latest/index.html'''
  class mouse (): 
    ''' Lưu toàn bộ các lệnh liên quan đến việc dùng chuột. '''
    class effect():
      ''' Các hiệu ứng di chuyển chuột.
      Ex: pyautogui.moveTo(100, 100, 2, pyautogui.easeInOutQuad)  # start and end fast, slow in middle.
      PIC: Components/PIC/mouseEffect.png
      https://www.google.com/search?q=easeInOutBounce&tbm=isch&ved=2ahUKEwiMuM2c_YL4AhURx4sBHV4oDWYQ2-cCegQIABAA&oq=easeInOutBounce&gs_lcp=CgNpbWcQDFAAWABgAGgAcAB4AIABAIgBAJIBAJgBAKoBC2d3cy13aXotaW1n&sclient=img&ei=jn6SYoy5BJGOr7wP3tC0sAY&bih=749&biw=1440#imgrc=9IWKOTyhZpwlgM
      '''
      easeInBack = pyautogui.easeInBack 
      '''Đây là phần viết lại chỉ dẫn cho hàm easeInBack'''
      
      easeInBounce = pyautogui.easeInBounce
      '''Đây là phần viết lại chỉ dẫn cho hàm easeInBounce'''
      
      easeInCirc = pyautogui.easeInCirc 
      '''Đây là phần viết lại chỉ dẫn cho hàm easeInCirc'''
      
      easeInCubic = pyautogui.easeInCubic 
      '''Đây là phần viết lại chỉ dẫn cho hàm easeInCubic'''
      
      easeInElastic = pyautogui.easeInElastic 
      '''Đây là phần viết lại chỉ dẫn cho hàm easeInElastic'''
      
      easeInExpo = pyautogui.easeInExpo 
      '''Đây là phần viết lại chỉ dẫn cho hàm easeInExpo'''
      
      easeInOutBack = pyautogui.easeInOutBack 
      '''Đây là phần viết lại chỉ dẫn cho hàm easeInOutBack'''
      
      easeInOutBounce = pyautogui.easeInOutBounce 
      '''Đây là phần viết lại chỉ dẫn cho hàm easeInOutBounce'''
      
      easeInOutCirc = pyautogui.easeInOutCirc
      easeInOutCubic = pyautogui.easeInOutCubic
      easeInOutElastic = pyautogui.easeInOutElastic
      easeInOutExpo = pyautogui.easeInOutExpo
      easeInOutQuad = pyautogui.easeInOutQuad
      easeInOutQuart = pyautogui.easeInOutQuart
      easeInOutQuint = pyautogui.easeInOutQuint
      easeInOutSine = pyautogui.easeInOutSine
      easeInQuad = pyautogui.easeInQuad
      easeInQuart = pyautogui.easeInQuart
      easeInQuint = pyautogui.easeInQuint
      easeInSine = pyautogui.easeInSine
      easeOutBack = pyautogui.easeOutBack
      easeOutBounce = pyautogui.easeOutBounce
      easeOutCirc = pyautogui.easeOutCirc
      easeOutCubic = pyautogui.easeOutCubic
      easeOutElastic = pyautogui.easeOutElastic
      easeOutExpo = pyautogui.easeOutExpo
      easeOutQuad = pyautogui.easeOutQuad
      easeOutQuart = pyautogui.easeOutQuart
      easeOutQuint = pyautogui.easeOutQuint
      easeOutSine = pyautogui.easeOutSine
      linear = pyautogui.linear
    
    click = pyautogui.click
    doubleClick = pyautogui.doubleClick
    drag = pyautogui.drag
    dragRel = pyautogui.dragRel
    dragTo = pyautogui.dragTo
    hscroll = pyautogui.hscroll
    leftClick = pyautogui.leftClick
    mouseDown = pyautogui.mouseDown
    mouseInfo = pyautogui.mouseInfo
    mouseUp = pyautogui.mouseUp
    move = pyautogui.moveTo
    moveRel = pyautogui.moveRel
    moveTo = pyautogui.moveTo
    rightClick = pyautogui.rightClick
    scroll = pyautogui.scroll
    '''
    `clicks`: Đơn vị lăn chuột.
      + `100`: Lăn lên 100 đơn vị.
      + `-100`: Lăn xuống 100 đơn vị.
    `x`: Vị trí contrỏ đặt trước khi lăn.
    `y`: Vị trí contrỏ đặt trước khi lăn.
    `CHÚ Ý`: Giá trị clicks không cần tăng lên nếu lăn xuống(lên) liên tục.
    `EX`: pyautogui.scroll(-200, 800, 600) #Đặt con trỏ tại vị trí (800, 600) sau đó lăn xuống 200 đơn vị.
    '''
    tripleClick = pyautogui.tripleClick
    vscroll = pyautogui.vscroll
    middleClick = pyautogui.middleClick

  class key (): 
    hold = pyautogui.hold
    hotkey = pyautogui.hotkey
    isShiftCharacter = pyautogui.isShiftCharacter
    isValidKey = pyautogui.isValidKey
    keyDown = pyautogui.keyDown
    keyUp = pyautogui.keyUp
    press = pyautogui.press
    typewrite = pyautogui.typewrite
    write = pyautogui.write
    
  class screen ():
    locate = pyautogui.locate
    locateAll = pyautogui.locateAll
    locateAllOnScreen = pyautogui.locateAllOnScreen
    locateCenterOnScreen = pyautogui.locateCenterOnScreen
    locateOnScreen = pyautogui.locateOnScreen
    locateOnWindow = pyautogui.locateOnWindow
    onScreen = pyautogui.onScreen
    pixel = pyautogui.pixel
    pixelMatchesColor = pyautogui.pixelMatchesColor
    screenshot = pyautogui.screenshot

  class system ():
    class window ():
      if WINDOW: getWindowsAt =pyautogui.getWindowsAt
      if WINDOW: getWindowsWithTitle =pyautogui.getWindowsWithTitle
      if WINDOW: getActiveWindow =pyautogui.getActiveWindow
      if WINDOW: getActiveWindowTitle =pyautogui.getActiveWindowTitle
      if WINDOW: getAllTitles =pyautogui.getAllTitles
      if WINDOW: getAllWindows =pyautogui.getAllWindows
    getInfo =pyautogui.getInfo
    size =pyautogui.size
    center =pyautogui.center
    run =pyautogui.run
    sleep =pyautogui.sleep
    countdown =pyautogui.countdown
    displayMousePosition =pyautogui.displayMousePosition
    getPointOnLine =pyautogui.getPointOnLine
    position =pyautogui.position
    printInfo =pyautogui.printInfo
    print_function =pyautogui.print_function
    failSafeCheck =pyautogui.failSafeCheck
    raisePyAutoGUIImageNotFoundException =pyautogui.raisePyAutoGUIImageNotFoundException
    useImageNotFoundException =pyautogui.useImageNotFoundException
    # Lib_Sys =pyautogui.sys
    # Lib_Time =pyautogui.time
    # Lib_Pyscreeze =pyautogui.pyscreeze
    # Lib_Mouseinfo =pyautogui.mouseinfo
    # Lib_Os =pyautogui.os
    # Lib_Platform =pyautogui.platform
    # Lib_PlatformModule =pyautogui.platformModule
    # functools =pyautogui.functools
    # Lib_Re =pyautogui.re
    # Lib_Datetime =pyautogui.datetime
    # Lib_Collections =pyautogui.collections