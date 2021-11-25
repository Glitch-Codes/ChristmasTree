import cv2
from time import sleep
from rpi_ws281x import *
import random
import decimal 

scanRadius = 3
similarity = 20
sleepTime = 2 # Starts out doulbe the length so the first LED will be on in time
coordList = []


cam = cv2.VideoCapture(0)
cam.set(3, 1280)  
cam.set(4, 720) 
cam.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
cam.set(cv2.CAP_PROP_BRIGHTNESS, 0.12) 
cam.set(cv2.CAP_PROP_EXPOSURE, 0.1)
cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# LED strip configuration:
LED_COUNT      = 16      
LED_PIN        = 18      
LED_FREQ_HZ    = 800000  
LED_DMA        = 10      
LED_BRIGHTNESS = 50   
LED_INVERT     = False   
LED_CHANNEL    = 0  
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Define function to wipe all LED data
def colorWipe(strip, color, wait_ms):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, color)
        strip.show()
        sleep(wait_ms/1000.0)
colorWipe(strip, Color(0,0,0), 10)

print("Press Space Bar to Start")

while True:
    ret, preview = cam.read()
    if not ret:
        print("Failed to grab preview, closing...")
        break
    cv2.normalize(preview, preview, 0, 255, cv2.NORM_MINMAX)
    cv2.imshow("Calibrate", preview)

    k = cv2.waitKey(1)
    if k%256 == 27:
        colorWipe(strip, Color(0,0,0), 10)
        print("Escape hit, closing...")
        break
    elif k%256 == 32:  
        cv2.destroyAllWindows()
        print("Clearing coords.txt")
        open('coords.txt', 'w').close()
        for c in range(2):
            if c == 0:
                for i in range(LED_COUNT):
                    cam.release()
                    print('Turning on LED ' + str(i))
                    strip.setPixelColor(i, Color(255,255,255))
                    strip.show()
                    print('Buffering frame... ')
                    sleep(sleepTime)
                    
                    cam = cv2.VideoCapture(0)
                    cam.set(3, 1280)  
                    cam.set(4, 720) 
                    cam.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
                    cam.set(cv2.CAP_PROP_BRIGHTNESS, 0.12) 
                    cam.set(cv2.CAP_PROP_EXPOSURE, 0.1)
                    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    ret2, frame = cam.read()
                    if not ret2:
                        print("Failed to grab preview, closing...")
                        break
                    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)

                    img_name = "calibrate_frame_XY_{}.png".format(i)
                    naive = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    robust = cv2.GaussianBlur(naive, (scanRadius, scanRadius), 0)
                    naivePos = cv2.minMaxLoc(naive)
                    robustPos = cv2.minMaxLoc(robust)
                    print("Naive XY Coords: " + str(naivePos[3]))
                    print("Robust XY Coords: " + str(robustPos[3]))

                    if (robustPos[3][0] - similarity) <= naivePos[3][0] <= (robustPos[3][0] + similarity) and (robustPos[3][1] - similarity) <= naivePos[3][1] <= (robustPos[3][1] + similarity):
                        cv2.circle(frame, robustPos[3], 1, (255, 100, 0), 2)
                        cv2.line(frame, robustPos[3], (robustPos[3][0], 0), (255, 100, 0), 1)
                        cv2.line(frame, robustPos[3], (0, robustPos[3][1]), (255, 100, 0), 1)
                        cv2.putText(frame,str(robustPos[3]), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0))
                        coordList.insert(len(coordList),str(robustPos[3]).replace("(", "[").replace(")", ""))
                        cv2.imwrite("photos/"+img_name, frame)
                        print("Position Compare Success: {}".format(img_name))
                    else: 
                        cv2.circle(frame, naivePos[3], 1, (0, 255, 0), 2)
                        cv2.line(frame, naivePos[3], (naivePos[3][0], 0), (0, 255, 0), 1)
                        cv2.line(frame, naivePos[3], (0, naivePos[3][1]), (0, 255, 0), 1)
                        cv2.circle(frame, robustPos[3], scanRadius, (255, 100, 0), 2)
                        cv2.line(frame, robustPos[3], (robustPos[3][0], 0), (255, 100, 0), 1)
                        cv2.line(frame, robustPos[3], (0, robustPos[3][1]), (255, 100, 0), 1)
                        cv2.putText(frame, "Naive: " + str(naivePos[3]), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                        cv2.putText(frame, "Robust: " + str(robustPos[3]), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0))
                        coordList.insert(len(coordList),str(robustPos[3]).replace("(", "[").replace(")", ""))
                        cv2.imwrite("photos/"+img_name, frame)
                        print("Position Compare Out Of Range: {}".format(img_name))
                    print('Turning off LED ' + str(i) + '\n')
                    strip.setPixelColor(i, Color(0,0,0))
                    strip.show()
                    sleep(sleepTime)
            
            if c == 1:
                input("Rotate the tree 90 degrees then press Enter...")
                for i in range(LED_COUNT):
                    cam.release()
                    print('Turning on LED ' + str(i))
                    strip.setPixelColor(i, Color(255,255,255))
                    strip.show()
                    print('Buffering frame... ')
                    sleep(sleepTime)
                    
                    cam = cv2.VideoCapture(0)
                    cam.set(3, 1280)  
                    cam.set(4, 720) 
                    cam.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
                    cam.set(cv2.CAP_PROP_BRIGHTNESS, 0.12) 
                    cam.set(cv2.CAP_PROP_EXPOSURE, 0.1)
                    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    ret2, frame = cam.read()
                    if not ret2:
                        print("Failed to grab preview, closing...")
                        break
                    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)

                    img_name = "calibrate_frame_Z_{}.png".format(i)
                    naive = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    robust = cv2.GaussianBlur(naive, (scanRadius, scanRadius), 0)
                    naivePos = cv2.minMaxLoc(naive)
                    robustPos = cv2.minMaxLoc(robust)
                    print("Naive Z Coord: " + str(naivePos[3][0]))
                    print("Robust Z Coord: " + str(robustPos[3][0]))

                    if (robustPos[3][0] - similarity) <= naivePos[3][0] <= (robustPos[3][0] + similarity) and (robustPos[3][1] - similarity) <= naivePos[3][1] <= (robustPos[3][1] + similarity):
                        cv2.circle(frame, robustPos[3], 1, (255, 100, 0), 2)
                        cv2.line(frame, robustPos[3], (robustPos[3][0], 0), (255, 100, 0), 1)
                        cv2.line(frame, robustPos[3], (0, robustPos[3][1]), (255, 100, 0), 1)
                        cv2.putText(frame, str(robustPos[3]), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 255))
                        with open('coords.txt', 'a') as coords:
                            coords.write((tuple(coordList)[i]) + ", " + str(robustPos[3][0]) + "]\n")
                        cv2.imwrite("photos/"+img_name, frame)
                        print("Position Compare Success: {}".format(img_name))
                    else: 
                        cv2.circle(frame, naivePos[3], 1, (0, 255, 0), 2)
                        cv2.line(frame, naivePos[3], (naivePos[3][0], 0), (0, 255, 0), 1)
                        cv2.line(frame, naivePos[3], (0, naivePos[3][1]), (0, 255, 0), 1)
                        cv2.circle(frame, robustPos[3], scanRadius, (255, 100, 0), 2)
                        cv2.line(frame, robustPos[3], (robustPos[3][0], 0), (255, 100, 0), 1)
                        cv2.line(frame, robustPos[3], (0, robustPos[3][1]), (255, 100, 0), 1)
                        cv2.putText(frame, "Naive: " + str(naivePos[3]), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                        cv2.putText(frame, "Robust: " + str(robustPos[3]), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0))
                        with open('coords.txt', 'a') as coords:
                            coords.write((tuple(coordList)[i]) + ", " + str(robustPos[3][0]) + "]\n")
                        cv2.imwrite("photos/"+img_name, frame)
                        print("Position Compare Out Of Range: {}".format(img_name))
                    print('Turning off LED ' + str(i) + '\n')
                    strip.setPixelColor(i, Color(0,0,0))
                    strip.show()    
                    sleep(sleepTime)
        