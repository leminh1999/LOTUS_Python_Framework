import __init
from Library.A8_Appium.appium_Wrap import appium_Remap
from time import sleep
from datetime import datetime
from Library.A2_LOTUS.lotus_Wrap import rgb,lotus_Remap as LOTUS
  
MOBI = appium_Remap()
# MOBI.setup.begin(remoteAddr="localhost",remotePort=4723,deviceUUID="LHS7N18B29003666")

desired_caps = {
    "uuid": "emulator-5554",                       # 🔴 ID của máy ảo/điện thoại thật. Lấy bằng lệnh "adb devices"
    "platformName": "Android",                     # 🔴 Tên hệ điều hành
    'newCommandTimeout': 300,                      # 🔴 Appium Server sẽ kill session nếu client không gửi request trong 300s
    #Trong Window chạy lệnh sau để lấy appPackage và appActivity của ứng dụng: adb shell dumpsys window windows | find "mCurrentFocus"
    # "appPackage": "com.ss.android.ugc.trill",                         # ⛔CHÚ Ý: Khi gắn appPackage và appActivity thì các icon trên màn hình sẽ bị kéo về vị trí gốc của nó.
    # "appActivity": "com.ss.android.ugc.aweme.splash.SplashActivity"   # ⛔Sẽ thay đổi vị trí và thư mục mà USER đã sắp xếp trên màn hình
}
MOBI.setup.begin("localhost",4723,desired_caps)


print("=== PROGRAM START ===")
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)


MOBI.button.home() # Ấn nút HOME
MOBI.fingerKey.tap('xpath=//android.widget.TextView[@content-desc="TikTok"]') # Mở ứng dụng TikTok
MOBI.others.others_clearReqWaitCmdFlg()
MOBI.fingerKey.tapPos(100,100) # Ấn vào vị trí (100,100)
while True:
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.fingerKey.longTap('id=com.ss.android.ugc.trill:id/ele') # Bỏ qua cửa sổ "Đăng nhập" nếu có
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.fingerKey.longTap('id=com.ss.android.ugc.trill:id/elf').screenshot("screenshot1.png")
  MOBI.others.others_clearReqWaitCmdFlg()
  # LOTUS.log.addClickPosToHtmlLog(pos["x"],pos["y"]);sleep(0.5) 











  


