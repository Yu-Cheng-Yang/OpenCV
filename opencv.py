import cv2
import numpy as np
# from PIL import Image
imgWidth = 640
imgHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, imgWidth)
cap.set(4, imgHeight)
cap.set(10, 150)


def preProcessing(img):

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5),1)
    imgCanny = cv2.Canny(imgBlur,200,200)
    kernel= np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
    imgThres = cv2.erode(imgDial,kernel,iterations=1)

    return imgThres
def getContours(img):
    biggest=np.array([])
    maxArea = 0
    contours, hierarchy =cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        # print(area)
        if area>500:
            #cv2.drawContours(imgContour,cnt, -1, (255,0,0),3)
            peri=cv2.arcLength(cnt, True)
            approx =cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) ==4:
                biggest = approx
                maxArea = area

    cv2.drawContours(imgContour,biggest, -1, (255,0,0),10)

    return biggest
def reorder(myPoints):
    myPoints=myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2), np.int32)
    add = myPoints.sum(1)
    print("add", add)
def getWarp(img, biggest):
    #reorder(biggest)
    pts1=np.float32(biggest)
    pts2=np.float32([[0,0],[imgWidth,0], [0, imgHeight], [imgWidth,imgHeight]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgOutput=cv2.warpPerspective(img,matrix, (imgWidth, imgHeight))
    return imgOutput
while True:
    success, img = cap.read()
    img=cv2.resize(img, (imgWidth,imgHeight))
    imgContour = img.copy()
    imgThres = preProcessing(img)
    getContours(imgThres)
    #imgWarped = getWarp(img, biggest)
    cv2.imshow("Result", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#image conversion

# image1 = Image.open(r'path where the image is stored\file name.png')
# im1 = image1.convert('RGB')
# im1.save(r'path where the pdf will be stored\new file name.pdf')