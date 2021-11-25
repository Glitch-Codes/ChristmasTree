from time import sleep
import cv2

cam = cv2.VideoCapture(0)
cam.set(3, 1280)  
cam.set(4, 720) 
cam.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
cam.set(cv2.CAP_PROP_BRIGHTNESS, 0.1) 
cam.set(cv2.CAP_PROP_EXPOSURE, 0.1)

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame, closing...")
        break
    cv2.imshow("LED Test", frame)
    
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

