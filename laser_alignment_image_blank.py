from picamera2 import Picamera2
import numpy as np
import time
import cv2

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (1280, 720), "format": "BGR888"})
picam2.configure(config)
picam2.start()

time.sleep(1)

d = input("Please enter distance from wall, in inches: ")
print("Confirming the distance you entered is:", d)

while True:
    image = picam2.capture_array()
    image = cv2.flip(image, -1)

    cv2.line(image, (640, 0), (640, 720), (0, 150, 150), 1)
    cv2.line(image, (600, 360), (1280, 360), (0, 150, 150), 1)

    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    red = (0, 0, 255)
    cv2.putText(image, str(d), (800, 200), font, 10, red, 10)

    cv2.imshow("Image", image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord("m"):
        filename = f"{int(d)}.jpg"
        cv2.imwrite(filename, image)
        break

cv2.destroyAllWindows()
picam2.stop()
