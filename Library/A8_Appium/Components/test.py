from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import MobileBy
import time

# Set up desired capabilities
desired_caps = {
    # Set your desired capabilities
}

# Initialize the Appium driver
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# Start recording the screen with custom parameters
video_options = {
    'timeLimit': '180',
    'bitRate': '4000000',
    'videoSize': '720x1280',
    'bugReport': 'true',
    'androidQuality': '20',
    'ignoreSilentMode': 'false'
}
driver.start_recording_screen(videoOptions=video_options)

# Perform your test actions
# ...

# Stop recording and save the video
video_data = driver.stop_recording_screen()
with open('recording.mp4', 'wb') as video_file:
    video_file.write(video_data)