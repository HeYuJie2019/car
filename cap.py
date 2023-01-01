import cv2
import time
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    a = cv2.waitKey(20)
    if a == 27:
        cv2.imwrite('pic/wl12.jpg', frame)
        cv2.destroyAllWindows()
        cap.release()
        break