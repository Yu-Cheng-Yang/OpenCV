
import cv2
import numpy as np
import os
import img2pdf as converter
from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
from tkinterdnd2 import *
from tkinterDnD import *
from dragdroplistbox import DragDropListbox
os.chdir(r"C:\Users\Yucheng\Documents\Python\opencv")
imgWidth = 480*2
imgHeight = 640*2
#
# for image in os.listdir(r"C:\Users\Yucheng\Documents\Python\opencv\inputs"):
#     inputlist=[]
#     scannedimage = os.path.join(r"C:\Users\Yucheng\Documents\Python\opencv\inputs", image)
#     print(scannedimage)
#     inputlist.append([cv2.imread(scannedimage)])
#     # for i in inputlist:
#     #     cv2.imshow("result1", i)
#     #     cv2.waitKey(0)
#
# print(len(inputlist))
# cap = cv2.imread('paper.jpg', cv2.IMREAD_UNCHANGED)
# cv2.resize(cap, (imgWidth,imgHeight), interpolation = cv2.INTER_AREA)




def preProcessing(img):

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5),1)
    imgCanny = cv2.Canny(imgBlur,200,200)
    kernel= np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
    imgThres = cv2.erode(imgDial,kernel,iterations=1)


    return imgThres
def getContours(img,imgContour):
    biggest=np.array([])
    maxArea = 0
    contours, hierarchy =cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area=cv2.contourArea(cnt)

        if area>5000:
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

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew



def getWarp(img, biggest):
    biggest=reorder(biggest)
    pts1=np.float32(biggest)
    pts2=np.float32([[0,0],[imgWidth,0], [0, imgHeight], [imgWidth,imgHeight]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgOutput=cv2.warpPerspective(img,matrix, (imgWidth, imgHeight))
    return imgOutput



def saveimage(img,currentcount):
    os.chdir(tempdirOut)
    cv2.imwrite('outputimage'+str(currentcount)+'.jpg', img)
    os.chdir(tempdirOut)
def savetopdf():
    imagelist=[]
    outputDirectory = tempdirOut

    for image in os.listdir(outputDirectory):
        f = os.path.join(outputDirectory, image)
        imagelist.append(f)


    os.chdir(r"C:\Users\Yucheng\Documents\Python\opencv\pdf results")
    outputpdf = open('scannedpdf.pdf', 'wb')
    outputpdf.write(converter.convert(imagelist))
    outputpdf.close()
    os.chdir(r"C:\Users\Yucheng\Documents\Python\opencv")
    print("Pdf conversion successful!")
def defaultconvert():
    imgCount = 0
    for image in os.listdir(r"C:\Users\Yucheng\Documents\Python\opencv\inputs"):
        scannedimage = os.path.join(r"C:\Users\Yucheng\Documents\Python\opencv\inputs", image)

        inputimage=cv2.imread(scannedimage)
        img=cv2.resize(inputimage, (imgWidth,imgHeight))
        imgContour = img.copy()
        imgThres = preProcessing(img)
        biggest=getContours(imgThres,imgContour)
        imgWarped = getWarp(img, biggest)

        saveimage(imgWarped,imgCount)
        imgCount+=1


        # cv2.imshow("Result", imgWarped)
        # cv2.waitKey(0)

    savetopdf()

def pageOrder(list,input,currentpage):
    if len(list)==currentpage:
        list.append(input)
    elif len(list)!=currentpage:
        del list[currentpage]
        list.insert(currentpage,input)
#
# def display_selected(choice):
#     choice = globals()['menuInput'+str(i)].get()
# def getListBoxEntr

def getInputDirectory():
    global tempdir
    global imageBox
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    directoryDisplayIn.configure(text= tempdir)
    imageBox = DragDropListbox(root)
    for i, image in enumerate(os.listdir(tempdir)):
        imageBox.insert(i, image)
    imageBox.grid(row=2, column=0,sticky="nsew")
    selectedImage=imageBox.bind('<<ListboxSelect>>', displayImage)
    imageBox.drop_target_register(DND_FILES)
    imageBox.dnd_bind('<<Drop>>', addto_listbox)
    default_convert_button.configure(text="Convert in list order", command=getListBoxElements)

    # default_convert_button.bind('<<Count>>', getListBoxElements)



def getOutputDirectory():
    global tempdirOut
    currdir = os.getcwd()
    tempdirOut = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    directoryDisplayOut.configure(text = tempdirOut)


def displayImage(event):
    global scannedImage
    global resized
    selection = event.widget.curselection()
    index = selection[0]
    value = event.widget.get(index)

    result.set(value)

    scannedImage = Image.open(os.path.join(tempdir, value))
    #print(type(imageDisplay))
    # currentinput=value
    resized= ImageTk.PhotoImage(scannedImage.resize((240,320)))
    imageDisplay.configure(image=resized)

def getListBoxElements():
    global numberListBoxElement
    global inputimage
    numberListBoxElement =[]
    for i in range(0,imageBox.size()):
        numberListBoxElement.append(imageBox.get(i))
    imgCount = 0

    imgCount = 0
    for image in numberListBoxElement:
        scannedimage = os.path.join(tempdir, image)

        inputimage=cv2.imread(scannedimage)
        img=cv2.resize(inputimage, (imgWidth,imgHeight))
        imgContour = img.copy()
        imgThres = preProcessing(img)
        biggest=getContours(imgThres,imgContour)
        imgWarped = getWarp(img, biggest)

        saveimage(imgWarped,imgCount)
        imgCount+=1


        # cv2.imshow("Result", imgWarped)
        # cv2.waitKey(0)

    savetopdf()

def addto_listbox(event):
    imageBox.insert("end", event.data)

root=TkinterDnD.Tk()
root.iconbitmap(r'C:\Users\Yucheng\Documents\Python\opencv\icon.ico')
#root.geometry("800x800")
result =StringVar()

tempdir=r"C:\Users\Yucheng\Documents\Python\opencv\inputs"
tempdirOut=r"C:\Users\Yucheng\Documents\Python\opencv\outputs"



root.title("Conversion of images to pdf")
imageCount=0
currentinput=0
inputList=[]

"""
initializing page choices
"""
initialImage=Image.open(os.path.join(r"C:\Users\Yucheng\Documents\Python\opencv\inputs\paper.jpg"))
resizedImage=ImageTk.PhotoImage(initialImage.resize((240,320)))


browseButton = Button(root, text="Browse for input folder", command=getInputDirectory).grid(row=0, column=1,sticky="nsew")
browseButton2 = Button(root, text="Browse for output folder", command=getOutputDirectory).grid(row=1, column=1,sticky="nsew")

Grid.rowconfigure(root, 0, weight=1)
Grid.rowconfigure(root, 1, weight=1)
Grid.rowconfigure(root, 2, weight=1)
Grid.rowconfigure(root, 3, weight=1)
Grid.columnconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 1, weight=1)
directoryDisplayIn = Label(root, text= tempdir)
directoryDisplayIn .grid(row=0, column=0)
directoryDisplayOut = Label(root, text= tempdirOut)
directoryDisplayOut.grid(row=1, column=0)


default_convert_button = Button(root, text="Convert in default order", command=defaultconvert)
default_convert_button.grid(row=3, column=1, sticky="nsew")

quit_button = Button(root, text="Cancel", command=root.quit)
quit_button.grid(row=3,column=0,sticky="nsew")
imageDisplay = Label(image=resizedImage)
imageDisplay.grid(row=2, column=1,sticky="nsew")



root.mainloop()

