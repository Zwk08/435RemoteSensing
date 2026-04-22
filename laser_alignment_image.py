# ENME489Y: Remote Sensing

from picamera2 import Picamera2
import numpy as np
import time
import cv2

# initialize the camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (1280, 720), "format": "BGR888"}
)
picam2.configure(config)
picam2.start()

# allow the camera to setup
time.sleep(1)

# grab images continuously
while True:
    image = picam2.capture_array()

    # may need to flip image, depending on mechanical setup of instrument
    image = cv2.flip(image, -1)

    # plot crosshairs, for alignment
    cv2.line(image, (640, 0), (640, 720), (0, 150, 150), 1)
    cv2.line(image, (0, 360), (1280, 360), (0, 150, 150), 1)

    # plot green vertical lines, for alignment
    for i in range(50, 1300, 50):
        cv2.line(image, (i, 0), (i, 720), (0, 150, 0), 3)

    # display the image on screen and wait for a keypress
    cv2.imshow("Image", image)
    key = cv2.waitKey(1) & 0xFF

    # break out of video loop when specified by the user
    if key == ord("q"):
        break

cv2.destroyAllWindows()
picam2.stop()
