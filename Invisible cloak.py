import cv2
import numpy as np
import time

capture_video = cv2.VideoCapture(0)  

time.sleep(2)

background = 0
for i in range(60):
    ret, background = capture_video.read()
background = np.flip(background, axis=1)  

while capture_video.isOpened():
    ret, img = capture_video.read()
    if not ret:
        break
    img = np.flip(img, axis=1) 

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_pink = np.array([140, 80, 80])   # H, S, V
    upper_pink = np.array([170, 255, 255])

    mask = cv2.inRange(hsv, lower_pink, upper_pink)


    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)

    mask_inv = cv2.bitwise_not(mask)

    res1 = cv2.bitwise_and(background, background, mask=mask)

    res2 = cv2.bitwise_and(img, img, mask=mask_inv)

    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("Invisible Cloak", final_output)

    if cv2.waitKey(10) == 27:
        break

capture_video.release()
cv2.destroyAllWindows()
