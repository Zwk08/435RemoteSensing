import cv2
from picamera2 import Picamera2
from datetime import datetime

picam2 = Picamera2()

# Set preview configuration
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

try:
    while True:
        # Grab the current date & time for a new filename
        now = datetime.now()
        today = now.strftime("%d-%m-%Y-%H_%M_%S")
        
        # Capture image
        image = picam2.capture_array()
        
        # Show live camera feed
        #cv2.imshow("Camera", image)
        
        # Wait 10 ms and check for key presses
        key = cv2.waitKey(10) & 0xFF
        
        if key == ord('s'):  # Save image
            cv2.imwrite(today + ".jpg", image)
            print(today)
            print("Image saved!")
        elif key == ord('q'):  # Quit
            break

finally:
    # Cleanup resources
    cv2.destroyAllWindows()
    picam2.stop()
    picam2.close()
