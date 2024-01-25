from appium import webdriver # Nhập thư viện appium

desired_caps = {
    # "uuid": "emulator-5554",        # ID của máy ảo/điện thoại thật
    "uuid": "LHS7N18B29003666",       # 🔴 ID của máy ảo/điện thoại thật
    # "uuid": "192.168.2.2:2222",       # 🔴 ID của máy ảo/điện thoại thật
    "platformName": "Android",        # 🔴 Tên hệ điều hành
    'newCommandTimeout': 300,         # 🔴 Appium Server sẽ kill session nếu client không gửi request trong 300s
    # 'appPackage': 'com.huawei.android.launcher',                         # ⛔CHÚ Ý: Khi gắn appPackage và appActivity thì các icon trên màn hình sẽ bị kéo về vị trí gốc của nó.
    # 'appActivity': 'com.huawei.android.launcher.unihome.UniHomeLauncher' # ⛔Sẽ thay đổi vị trí và thư mục mà USER đã sắp xếp trên màn hình
}
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps) # Khởi tạo một session với desired_caps
driver.implicitly_wait(30) # Cài đặt thời gian chờ cho element hiển thị (VD: trong 30s)
# element = driver.find_element("id", "com.google.android.googlequicksearchbox:id/search_edit_frame") # Tìm element theo ID và click vào element
# element.click() # Click vào element
# element = driver.find_element("id", "com.google.android.googlequicksearchbox:id/googleapp_search_box") # Tìm element theo ID và click vào element
# element.send_keys("Hello Appium") # Gửi dữ liệu vào element

######################################################################
import time, pprint
# driver.get_screenshot_as_file("screenshot1.png") # Chụp màn hình và lưu vào file screenshot.png

# driver.press_keycode(new KeyEvent(AndroidKey.HOME).withFlag(KeyEventFlag.PRESSURE_DOWN));
# print("1. Ấn nút MENU")
# driver.press_keycode(82) # Ấn nút MENU
# time.sleep(2)
# print("2. Ấn nút HOME")
# driver.press_keycode(3) # Ấn nút HOME
# time.sleep(2)

#Get input from keyboard then print it
while True:
    #print screen resolution
    print("Screen resolution: ", driver.get_window_size())
    
    inputString = input("Enter your input: ")
    print("Received input is: ", inputString)
    driver.press_keycode(int(inputString)) # Ấn nút HOME

# https://developer.android.com/reference/android/view/KeyEvent.html
#  26: POWER BUTTON (WORKING <-> SLEEP)
# 223: SLEEP BUTTON (WORKING/SLEEP -> SLEEP)
# 224: WAKE UP BUTTON (WORKING/SLEEP -> WORKING)
# 279: PASTE
# 278: COPY
# 115: CAPS_LOCK
#  93: PAGE_DOWN
#  92: PAGE_UP
#  66: ENTER BUTTON
# 164: VOLUME MUTE
#  24: VOLUME UP
#  25: VOLUME DOWN
#   3: HOME BUTTON
#   4: BACK/PREVIOUS (WEB)
# 125: FORWARD (WEB)
#  84: INPUT SEARCH URL (WEB)
# 135: F5 - RELOAD (WEB)
#   5: OPEN CALL (DANH BẠ)
#   6: END CALL -> Tắt screen
#  64: OPEN BROWSER (CHROME)
#  65: OPEN MAIL APP (GMAIL)
# 187: APP_SWITCH
# 284: ALL_APPS
# 219: GOOGLE_ASSISTANT
# 231: VOICE_ASSISTANT
# 220: BRIGHTNESS_DOWN
# 221: BRIGHTNESS_UP
# 208: OPEN CALENDAR
# 209: OPEN MUSIC APP
# 207: OPEN CONTACTS
# 168: ZOOM_IN (CAMERA)
# 169: ZOOM_OUT (CAMERA)
#  27: CLICK CAMERA CAPTURE BUTTON (CAMERA)











