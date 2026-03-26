from picamera2 import Picamera2, Preview
import cv2
import time

# Init camera
picam2 = Picamera2()

# Start a preview window (GUI)
picam2.start_preview(Preview.QTGL)

# Set up video size & color
config = picam2.create_video_configuration(main={"size":(640, 480),"format":"RGB888"})
picam2.configure(config)

picam2.set_controls({
    "AwbMode": 5,        # e.g., daylight white balance
    "Brightness": 0.5,
    "Contrast": 1.0,
    "Saturation": 1.2
})

# Start camera (after preview)
picam2.start()
time.sleep(0.1)  # warmup

# Set up OpenCV video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('stoplight.mp4', fourcc, 25, (640, 480))

start_time = time.time()
record_duration = 30  # seconds

while True:
    # get frame as RGB from picamera
    frame = picam2.capture_array()
    # convert to BGR for OpenCV
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # write to video
    out.write(frame_bgr)

    # optional: show frame in OpenCV window (your own preview)
    cv2.imshow("Frame", frame_bgr)
    key = cv2.waitKey(1) & 0xFF

    # break at 30s or on 'q'
    if (time.time() - start_time) > record_duration or key == ord("q"):
        break

# clean up
out.release()
cv2.destroyAllWindows()
picam2.stop()
