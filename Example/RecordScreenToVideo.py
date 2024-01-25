import cv2
import numpy as np
import pyautogui

# Set the screen size
screen_size = (1920, 1080)

# Set the output video file name
output_file = "output.avi"

# Set the frames per second (FPS)
fps = 15

# Create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(output_file, fourcc, fps, screen_size)

# Loop through the screen frames
import time
currentTime = time.time()
print("Screen recording started: ", currentTime)
while time.time() - currentTime < 5:
    # Capture the screen frame
    img = pyautogui.screenshot()

    # Convert the screen frame to a numpy array
    frame = np.array(img)

    # Convert the color from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Write the frame to the video file
    out.write(frame)

    # Display the resulting frame
    # cv2.imshow("Screen Recording", frame)

    # Stop recording when "q" key is pressed
    if cv2.waitKey(1) == ord("q"):
        break

print("Screen recording completed: ", time.time())
      
# Release the resources
out.release()
cv2.destroyAllWindows()


print("Screen recording completed")
from moviepy.editor import VideoFileClip

# Open the AVI video file
avi_file = "output.avi"
video = VideoFileClip(avi_file)

# Define the output file name and codec
mp4_file = "output.mp4"
codec = 'libx264'

# Convert the video to MP4 format
video.write_videofile(mp4_file, codec=codec)

# Close the video file
video.close()


print("Convert completed")