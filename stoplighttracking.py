# ENME 489Y: Remote Sensing

# Python script tracks green 'stoplight'
# and saves video of tracking to stoplight.mp4

# import the necessary packages

#from picamera.array import PiRGBArray
#from picamera import PiCamera
from picamera2 import Picamera2
import numpy as np
#import imutils
import cv2
import time

# define the lower and upper boundaries of the
# green circle in the HSV color space
# Note: use colorpicker.py to create a new HSV mask
colorLower = (29, 70, 6)
colorUpper = (75, 255, 255)

# initialize the Raspberry Pi camera
"""
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(640,480))
"""
picam2 = Picamera2()
# Video configuration (less crop than preview)
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)

# Optional: fix color tint
picam2.set_controls({
    "AwbMode": 5, # "Incandescent",   # or "Auto" / "Daylight" depending on your lighting
    "Brightness": 0.5,           # adjust if needed
    "Contrast": 1.0,
    "Saturation": 1.2             # slightly boost color if green looks dull
})
picam2.start()
# allow the camera to warmup
time.sleep(0.1)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('stoplight.mp4', fourcc, 25, (640, 480))

# --- Timing for recording ---
start_time = time.time()
record_duration = 32  # seconds (change if you want longer)

# define the codec and create VideoWriter object
# UNCOMMENT THE FOLLOWING TWO (2) LINES TO SAVE .avi VIDEO FILE
# TRY BOTH XVID THEN MJPG, IN THE EVENT THE .avi FILE IS NOT SAVING PROPERLY
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# out = cv2.VideoWriter('stoplight.avi',fourcc,10,(640, 480))


# keep looping
#for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
# grab the current frame
#image = frame.array
while True:
    #image = picam2.capture_array()
    request = picam2.capture_request()
    image = request.make_array("main")
    request.release()
    # blur the frame and convert to the HSV
    # color space
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)#make smaller for better fps
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # find counters in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    # proceed regardless to keep video streaming
    
    if len(cnts) > 0:

        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 0:
            # draw the circle and centroid on the frame
           	# then update the list of tracked points
            cv2.circle(image_bgr, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(image_bgr, center, 2, (0, 0, 255), -1)
            # write the frame to video file
            # UNCOMMENT THE FOLLOWING ONE (1) LINE TO SAVE .avi VIDEO FILE
    out.write(image_bgr)

    # show the frame to our screen
    cv2.imshow("Frame", image_bgr)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    #rawCapture.truncate(0)

    # press the 'q' key to stop the video stream
    if key == ord("q") or (time.time()- start_time)> record_duration:
        break
print("Recording finished")







