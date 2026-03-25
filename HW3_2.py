from picamera2 import Picamera2
import cv2
from datetime import datetime

picam2 = Picamera2()

# Use still configuration (works in VNC or headless)
picam2.configure(picam2.create_still_configuration(main={"size": (1280,720)}))
picam2.start()

try:
    print("Press 's' to save an image, 'q' to quit")
    while True:
        # Capture frame
        image = picam2.capture_array()

        # Show live preview
        cv2.imshow("Camera Preview", image)

        key = cv2.waitKey(50) & 0xFF
        if key == ord('s'):
            filename = "/home/pi/435RemoteSensing/" + datetime.now().strftime("%d-%m-%Y-%H_%M_%S") + ".jpg"
            cv2.imwrite(filename, image)
            print(f"Saved image as {filename}")
        elif key == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    picam2.stop()
    picam2.close()
