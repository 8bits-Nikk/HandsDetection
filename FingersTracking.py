import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderpath = "images"
myList = os.listdir(folderpath)
print(myList)

overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderpath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

cTime, pTime = 0, 0

detector = htm.HandDetector(max_hands=1)

tipIDs = [4, 8, 12, 16, 20]

while cap.isOpened():
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        print(lmList)

    if len(lmList) != 0:
        isOpen = []
    
        if lmList[tipIDs[0]][1] > lmList[tipIDs[0] - 1][1]:
            isOpen.append(1)
        else:
            isOpen.append(0)
    
        for id in range(1, 5):
            if lmList[tipIDs[id]][2] < lmList[tipIDs[id] - 2][2]:
                isOpen.append(1)
            else:
                isOpen.append(0)
    
        fingercount = isOpen.count(1)
        print(fingercount)
    
        h, w, c = overlayList[fingercount-1].shape
        img[0:h, 0:w] = overlayList[fingercount-1]

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (460, 60), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    cv2.imshow("CAM", img)
    cv2.waitKey(1)
