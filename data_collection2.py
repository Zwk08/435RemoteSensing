from picamera2 import Picamera2
import numpy as np
import time
import cv2
import os

# ---- SETUP CAMERA ----
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (1280, 720), "format": "BGR888"}
)
picam2.configure(config)
picam2.start()

time.sleep(1)

# ---- USER INPUT ----
d = input("Please enter IMU angle: ")
print("Confirming the IMU angle you entered is:", d)

# ---- CREATE SAVE FOLDER ----
save_dir = "/home/pi/alignment_images"
os.makedirs(save_dir, exist_ok=True)

# ---- MAIN LOOP ----
while True:
    image = picam2.capture_array()

    # flip image (same as -vf -hf)
    image = cv2.flip(image, -1)

    # draw crosshairs
    cv2.line(image, (640, 0), (640, 720), (0, 150, 150), 1)
    cv2.line(image, (600, 360), (1280, 360), (0, 150, 150), 1)

    # display distance text
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    red = (0, 0, 255)
    cv2.putText(image, str(d), (800, 200), font, 2, red, 2)

    # show image
    cv2.imshow("LiDAR Alignment", image)

    key = cv2.waitKey(1) & 0xFF

    # ---- SAVE IMAGE ----
    if key == ord("m"):
        filename = f"{save_dir}/{int(d)}.jpg"
        cv2.imwrite(filename, image)
        print("Saved:", filename)

    # ---- QUIT ----
    if key == ord("q"):
        print("Exiting...")
        break

# ---- CLEANUP ----
cv2.destroyAllWindows()
picam2.stop()
