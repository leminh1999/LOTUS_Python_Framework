import __init
from Library.A2_LOTUS.Components.LotusLib import *
import pyperclip

class lotus_Remap ():
  class log():
    saveClickImage = LotusLib.saveClickImage
    addClickPosToHtmlLog = LotusLib.addClickPosToHtmlLog
    addScreenCaptureToHtmlLog = LotusLib.addScreenCaptureToHtmlLog
    addRectScreenCaptureToHtmlLog = LotusLib.addRectScreenCaptureToHtmlLog
    addImageToHtmlLog = LotusLib.addImageToHtmlLog
    
    
  class wait():
    wait3Color = LotusLib.wait3Color
    wait3NotColor = LotusLib.wait3NotColor
    waitColor = LotusLib.waitColor
    waitNotColor = LotusLib.waitNotColor
    waitImage = LotusLib.waitImage
    waitNotImage = LotusLib.waitNotImage

    
  class color(wait):
    getColor = LotusLib.getColor
    horFindColor = LotusLib.horFindColor
    horFindColorFromPilImage = LotusLib.horFindColorFromPilImage
    verFindColor = LotusLib.verFindColor
    checkColorWithCapture = LotusLib.checkColorWithCapture
    checkColorWithoutCapture = LotusLib.checkColorWithoutCapture
  
  class convert():
    convertHumanNumToInt = LotusLib.convertHumanNumToInt
    convertToHour = LotusLib.convertToHour
  
  class time():
    getCurTime = LotusLib.getCurTime
    delay = LotusLib.delay
  
  class capture():
    captureToImageVar = LotusLib.captureToImageVar
    
  class imageAction():
    clickImage = LotusLib.clickImage
    findAllImageOnScreen = LotusLib.findAllImageOnScreen
    findAllImageRegionScreen = LotusLib.findAllImageRegionScreen
  
  class taskManager():
    taskKiller = LotusLib.taskKiller
    taskKillerEnd = LotusLib.taskKillerEnd
    taskKillerStart = LotusLib.taskKillerStart
    programOpenJoinIn = LotusLib.programOpenJoinIn
    programOpenParallel = LotusLib.programOpenParallel
    programTerminateConf = LotusLib.programTerminateConf
    
  class clipboard():
    pyperclip.set_clipboard('xsel')
    copyToClipboard = LotusLib.copyToClipboard
    pasteFromClipboard = LotusLib.pasteFromClipboard
    pasteFromClipboardToVar = LotusLib.pasteFromClipboardToVar
    pasteFromClipboardToVarBigData = LotusLib.pasteFromClipboardToVarBigData
    
  class others():
    keyDownPeriod = LotusLib.keyDownPeriod
    listDir = LotusLib.listDir
    midRec = LotusLib.midRec
    midRecInt = LotusLib.midRecInt

    restart = LotusLib.restart
    sendMsg = LotusLib.sendMsg
