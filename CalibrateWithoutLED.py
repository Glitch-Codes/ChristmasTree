import cv2
from time import *

cam = cv2.VideoCapture(0)

img_counter = 0

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
        cv2.destroyAllWindows()
        for c in range(2):
            if c == 0:
                for i in range(4):
                    print('Buffering frame... ')
                    ret, frame = cam.read()
                    if not ret:
                        print("Failed to grab frame, closing...")
                        break
                    print('Turning on LED ' + str(i))
                    sleep(1)

                    img_name = "calibrate_frame_{}.png".format(img_counter)
                    firstPass = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    secondPass = cv2.GaussianBlur(firstPass, (1, 1), 0)
                    firstPos = cv2.minMaxLoc(firstPass)
                    secondPos = cv2.minMaxLoc(secondPass)
                    print("First Pass Coord: " + str(firstPos[3]))
                    print("Second Pass Coord: " + str(secondPos[3]))

                    if firstPos[3] == secondPos[3]:
                        cv2.circle(frame, secondPos[3], 1, (0, 255, 0), 2)
                        cv2.line(frame, secondPos[3], (secondPos[3][0], 0), (0, 255, 0), 1)
                        cv2.line(frame, secondPos[3], (0, secondPos[3][1]), (0, 255, 0), 1)
                        cv2.putText(frame, "  " +str(secondPos[3]), (-10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                        with open('coords.txt', 'a') as coords:
                            coords.write(str(secondPos[3]).replace("(", "[").replace(")", "")+'\n')
                        cv2.imwrite("photos/"+img_name, frame)
                        print("{} written!".format(img_name))
                        img_counter += 1
                    else: 
                        with open('coords.txt', 'a') as coords:
                            coords.write('Unable to find LED ' + i + '\n')
                    print('Turning off LED ' + str(i))
                    sleep(1)
        
cam.release()
cv2.destroyAllWindows()