
import numpy as np
import cv2
from picamera2 import Picamera2
import time

# camera = cv2.VideoCapture('/dev/video0', cv2.CAP_FFMPEG)
# camera = cv2.VideoCapture(0)
# if not camera.isOpened():
#     camera.open('/dev/video0')

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (1640, 1232)})
picam2.configure(config)
picam2.start()

while 1:
    # Capture frame-by-frame
    captured_frame = picam2.capture_array("main")
    output_frame = captured_frame.copy()
    #
    # Convert original image to BGR, since Lab is only available from BGR
    captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)
    # First blur to reduce noise prior to color space conversion
    captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
    # Convert to Lab color space, we only need to check one channel (a-channel) for red here
    captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)
    # Threshold the Lab image, keep only the red pixels
    # Possible yellow threshold: [20, 110, 170][255, 140, 215]
    # Possible blue threshold: [20, 115, 70][255, 145, 120]
    # Possible red threshold: [20, 150, 150][190, 255, 255]
    captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([20, 115, 70]), np.array([255, 145, 120]))
    # Second blur to reduce more noise, easier circle detection
    captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
    # Use the Hough transform to detect circles in the image
    circles = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_red.shape[0] / 8, param1=100, param2=18, minRadius=2, maxRadius=0)

	# If we have extracted a circle, draw an outline
	# We only need to detect one circle here, since there will only be one reference object
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        cv2.circle(output_frame, center=(circles[0, 0], circles[0, 1]), radius=circles[0, 2], color=(0, 255, 0), thickness=2)

    # Display the resulting frame, quit with q
    cv2.imshow('frame', output_frame)
    # cv2.imwrite('frame.jpg', output_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
picam2.release()
cv2.destroyAllWindows()
