import cv2
from time import sleep
from rpi_ws281x import *

cam = cv2.VideoCapture(0)

scanRadius = 3
similarity = 20
coordList = []

# LED strip configuration:
LED_COUNT      = 10      
LED_PIN        = 18      
LED_FREQ_HZ    = 800000  
LED_DMA        = 10      
LED_BRIGHTNESS = 150     
LED_INVERT     = False   
LED_CHANNEL    = 0  
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Define function to wipe all LED data
def colorWipe(strip, color, wait_ms=50):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, color)
        strip.show()
        sleep(wait_ms/1000.0)
colorWipe(strip, Color(255,255,255), 10)

print("Press Space Bar to Start")

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame, closing...")
        break
    cv2.imshow("Calibrate", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:  
        colorWipe(strip, Color(0,0,0), 10)
        cv2.destroyAllWindows()
        print("Clearing coords.txt")
        open('coords.txt', 'w').close()
        for c in range(2):
            if c == 0:
                for i in range(LED_COUNT):
                    print('Buffering frame... ')
                    ret, frame = cam.read()
                    if not ret:
                        print("Failed to grab frame, closing...")
                        break
                    print('Turning on LED ' + str(i))
                    strip.setPixelColor(i, Color(255,255,255))
                    strip.show()
                    sleep(2) # Sleep to let the camera focus

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
                        print("Position Compare Success: {} \n".format(img_name))
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
                        print("Position Compare Out Of Range: {} \n".format(img_name))
                        cv2.imwrite("photos/"+img_name, frame)
                    print('Turning off LED ' + str(i))
                    strip.setPixelColor(i, Color(0,0,0))
                    strip.show()
                    sleep(1)
            
            if c == 1:
                input("Rotate the tree 90 degrees then press Enter...")
                for i in range(LED_COUNT):
                    print('Buffering frame... ')
                    ret, frame = cam.read()
                    if not ret:
                        print("Failed to grab frame, closing...")
                        break
                    print('Turning on LED ' + str(i))
                    strip.setPixelColor(i, Color(255,255,255))
                    strip.show()
                    sleep(1)

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
                        print("Position Compare Success: {} \n".format(img_name))
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
                        print("Position Compare Out Of Range: {} \n".format(img_name))
                        cv2.imwrite("photos/"+img_name, frame)
                    print('Turning off LED ' + str(i))
                    strip.setPixelColor(i, Color(0,0,0))
                    strip.show()
                    sleep(1)
        