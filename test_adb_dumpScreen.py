# import os
# import shutil

# # 1. adb shell screencap -p /sdcard/screenshot.png
# # 2. adb pull /sdcard/screenshot.png
# # 3. adb shell rm /sdcard/screenshot.png

# os.system("adb shell screencap -p /sdcard/screenshot.png")
# os.system("adb pull /sdcard/screenshot.png")
# os.system("adb shell rm /sdcard/screenshot.png")

import cv2
import numpy as np
import subprocess
import os


# os.system("adb shell screencap -p")

# exit()


def get_adb_devices():
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    output = result.stdout.strip()
    lines = output.split("\n")[1:]
    devices = [line.split("\t")[0] for line in lines if "\tdevice" in line]
    return devices

def capture_screen(device_id):
    print("Device ID: "+str(device_id))
    command = f"adb -s {device_id} exec-out screencap -p"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    screen_data, _ = process.communicate()
    return cv2.imdecode(np.frombuffer(screen_data, np.uint8), cv2.IMREAD_COLOR)

def capture_screen2(device_id):
    os.system("adb -s "+str(device_id)+" shell screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png")
  
def main():
    adb_devices = get_adb_devices()
    if not adb_devices:
        print("No connected Android devices found.")
        return

    # Connect to the first available device (you can modify this to choose a specific device)
    device_id = adb_devices[0]

    while True:
        # Capture the screen from the Android device
        # screen_np = capture_screen2(device_id)

        # Display the screen capture using OpenCV
        # cv2.imshow("Android Screen Stream", screen_np)
        
        capture_screen2(device_id)
        cv2.imshow("Android Screen Stream", cv2.imread("screenshot.png"))

        cv2.waitKey(1)
        # # Break the loop when 'q' is pressed
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # Close the OpenCV window
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
