from picamera2 import Picamera2
import cv2
from datetime import datetime

picam2 = Picamera2()

# Use still config at native sensor resolution to avoid zoomed crop
picam2.configure(picam2.create_still_configuration(main={"size": (1920,1080)}))
picam2.start()

try:
    while True:
        image = picam2.capture_array()
        
        # Convert RGB to BGR for OpenCV display
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow("Camera Preview", image_bgr)
        
        key = cv2.waitKey(50) & 0xFF
        if key == ord('s'):
            filename = "/home/pi/435RemoteSensing/" + datetime.now().strftime("%d-%m-%Y-%H_%M_%S") + ".jpg"
            cv2.imwrite(filename, image_bgr)
            print(f"Saved image as {filename}")
        elif key == ord('q'):
            break

finally:
    cv2.destroyAllWindows()
    picam2.stop()
    picam2.close()
