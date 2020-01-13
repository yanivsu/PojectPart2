import numpy as np
import math
from fpdf import FPDF
import cv2
import seaborn as sns
import matplotlib.pyplot as plt
from pdf2image import convert_from_path, convert_from_bytes
from matplotlib import pyplot, transforms
import matplotlib.image as mpimg
from scipy.ndimage.filters import gaussian_filter
import mongoDB as db
import webbrowser
import struct

def Main():
    print()
    durationTimeOnCatd('user8', 8)
    # print(db.GetNumberOfRoundByUsername('mnb'))
    # print('Please enter your userName')
    # db.DominatValue('Yaniv', 21)
    #HeatMapFunction('Gulkin', 14, 0)
    # print(db.GetCoordinateByRoundNumber('Gulkin', 1))
    # PointDrawing('Gulkin', 6)
    # SpeedUpEyes()
    # CreateCardBoard(db.GetBoard('mnb', 232))
    # PDF2Image()
    # CreateDominantCardBoard()
# MyPlot function helps to maps all the point into gaussian numbers
def getAnalysis(userName,roundNumber,analysisFlag):
    print()
    durationTimeOnCatd()
def createPirChart(durationTimeList):
    names = ("#1", "#2", "#3", "#4", "#5")
    scores = [durationTimeList[0], durationTimeList[1], durationTimeList[2],
              durationTimeList[3], durationTimeList[4]
            ]
    plt.axis("equal")
    plt.pie(scores,labels=names,autopct="%0.2f%%")
    plt.show()
def createBarChart(durationTimeList):
    fig = plt.figure(figsize=(7, 5))
    names = ("#1", "#2", "#3", "#4", "#5")
    scores = [durationTimeList[0], durationTimeList[1], durationTimeList[2],
              durationTimeList[3], durationTimeList[4],
          ]
    position = [0, 1, 2, 3, 4]
    plt.bar(position, scores, width=0.3)
    plt.xticks(position, names)
    plt.title("Gaze duration on cards")
    plt.xlabel("Cards")
    plt.ylabel("Time(sec)")
    plt.show()

def getNMaxElements(durationTimeList,N):
     final_list = []
     for i in range(0,N):
         max1 = 0
         for j in range(len(durationTimeList)):
            if durationTimeList[j] > max1:
             max1 = durationTimeList[j]
         durationTimeList.remove(max1)
         final_list.append(max1)
     return final_list

def durationTimeOnCatd(userName,userRound):
    durationTimeList=[0,0,0,0,0,0,0,0,0,0,0,0]
    maxNValues=[]
    print(durationTimeList)
    listOfCoodinate = db.GetCoordinateByRoundNumber(userName, int(userRound))
    xCor = listOfCoodinate[0]
    yCor = listOfCoodinate[1]
    for i in range(len(xCor)):
        xCor[i] = float(xCor[i])
    for i in range(len(yCor)):
        yCor[i] = float(yCor[i])

    durationTimeList=getEyesOnCardsData(xCor,yCor)
    maxNValues= getNMaxElements(durationTimeList,5)
    createBarChart(maxNValues)
    createPirChart(maxNValues)

def getEyesOnCardsData(xCor,yCor):
    durationTimeList=[0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(xCor)):
        # ---------------- FIRST ROW ----------------#
        ####### Card Number 1 #######
        if (xCor[i] > 400.0 and xCor[i] < 750.0 and yCor[i] > 250.0 and yCor[i] < 350.0):
            durationTimeList[0] = durationTimeList[0] + 0.085
            ####### Card Number 2 #######
        if (xCor[i] > 900.0 and xCor[i] < 1200.0 and yCor[i] > 250.0 and yCor[i] < 350.0):
            durationTimeList[1] = durationTimeList[1] + 0.085
        ####### Card Number 3 #######
        if (xCor[i] > 1300.0 and xCor[i] < 1600.0 and yCor[i] > 250.0 and yCor[i] < 350.0):
            durationTimeList[2] = durationTimeList[2] + 0.085
        # ---------------- SECEND ROW ----------------#
        ####### Card Number 4 #######
        if (xCor[i] > 400.0 and xCor[i] < 750.0 and yCor[i] > 380.0 and yCor[i] < 480.0):
            durationTimeList[3] = durationTimeList[3] + 0.085
            ####### Card Number 5 #######
        if (xCor[i] > 900.0 and xCor[i] < 1200.0 and yCor[i] > 380 and yCor[i] < 480.0):
            durationTimeList[4] = durationTimeList[4] + 0.085
            ####### Card Number 6 #######
        if (xCor[i] > 1300.0 and xCor[i] < 1600.0 and yCor[i] > 380 and yCor[i] < 480.0):
            durationTimeList[5] = durationTimeList[5] + 0.085
        # ---------------- THIRED ROW ----------------#
        ####### Card Number 7 #######
        if (xCor[i] > 400.0 and xCor[i] < 750 and yCor[i] > 490.0 and yCor[i] < 590.0):
            durationTimeList[6] = durationTimeList[6] + 0.085
            ####### Card Number 8 #######
        if (xCor[i] > 900 and xCor[i] < 1200 and yCor[i] > 490 and yCor[i] < 590):
            durationTimeList[7] = durationTimeList[7] + 0.085
            ####### Card Number 9 #######
        if (xCor[i] > 1300 and xCor[i] < 1600 and yCor[i] > 490 and yCor[i] < 590):
            durationTimeList[8] = durationTimeList[8] + 0.085
        # ---------------- FOURTH ROW ----------------#
        ####### Card Number 10 #######
        if (xCor[i] > 425 and xCor[i] < 725 and yCor[i] > 600 and yCor[i] < 700):
            durationTimeList[9] = durationTimeList[9] + 0.0085
            ####### Card Number 11 #######
        if (xCor[i] > 900 and xCor[i] < 1200 and yCor[i] > 600 and yCor[i] < 700):
            durationTimeList[10] = durationTimeList[10] + 0.0085
            ####### Card Number 12 #######
        if (xCor[i] > 1325 and xCor[i] < 1625 and yCor[i] > 600 and yCor[i] < 700):
            durationTimeList[11] = durationTimeList[11] + 0.0085
    return durationTimeList


def myplot(x, y, s, bins=1000):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent
def PointDrawing(userName,userRound):
    print("STARTING TO CREATE POINT DRAWING GRAPH")
    listOfCardByRound = db.GetBoard(userName, userRound)
    CreateCardBoard(listOfCardByRound)
    PDF2Image()
    listOfCoodinate = db.GetCoordinateByRoundNumber(userName, userRound)
    xCor = []
    yCor = []
    for x in listOfCoodinate[0]:
        xCor.append(float(x))
    for y in listOfCoodinate[1]:
        yCor.append(float(y))
    plt.plot(xCor, yCor, 'bo-')
    map_img = mpimg.imread('out.jpg')
    plt.imshow(map_img, zorder=0, extent=[0, 2006, 0, 960], aspect='auto')
    plt2PDF(plt)
    plt.show()
def HeatMapFunction(username,roundNumber,dominateFlag,analysisFlag):
    #  Connect to DB and create a Board
    if(dominateFlag==0):
      print("REGULAR BOARD HAS BEEN SELECTED TO BE CREATED")
      listOfCardByRound = db.GetBoard(username, int(roundNumber))
      CreateCardBoard(listOfCardByRound)
    if (dominateFlag == 1):
      print("DOMINATE BOARD HAS BEEN  SELECTED TO BE CREATED")
      listOfCardByRound = db.DominatValue(username, int(roundNumber))
      CreateDominantCardBoard(listOfCardByRound)
    PDF2Image()
    listOfCoodinate = db.GetCoordinateByRoundNumber(username, int(roundNumber))
    xCor = []
    yCor = []
    #  Convert String point to float point
    for x in listOfCoodinate[0]:
        xCor.append(float(x))
    for y in listOfCoodinate[1]:
        y = float(y)
        #  Calibrate the camera y axis for the image
        y -= 180
        yCor.append(float(y))
    plt.subplots(figsize=(12, 12))
    map_img = mpimg.imread('out.jpg')
    hmax = sns.kdeplot(xCor, yCor, cmap="Blues", shade=False)
    hmax.collections[0].set_alpha(0)
    #  Extent helps me to set the axis 0 =>2006 in
    # X axis and 960 => 0 in y axis
    plt.imshow(map_img, zorder=0, extent=[0, 2006, 960, 0], aspect='auto')
    #  Export File to PDF
    plt2PDF(plt)
    webbrowser.open_new(r'testPlot.pdf')
    plt.show()
def SpeedUpEyes(userName,userRound):
    print("STARTING TO CREATE SPEED EYE GRAPH")
    listOfCoodinate = db.GetCoordinateByRoundNumber(userName,userRound)
    xCor = []
    yCor = []
    #  Convert String point to float point
    for x in listOfCoodinate[0]:
        xCor.append(float(x))
    for y in listOfCoodinate[1]:
        yCor.append(float(y))
    timeOfRound = db.GetTimeDeatilsPerRound(userName, userRound)[1]
    pointsCount = xCor.__len__()
    deltaTimePerPoint = pointsCount / timeOfRound
    #Calcuate Distance
    distanceArray = []
    for i in range(len(xCor) - 1):
        firstPoint = [xCor[i], yCor[i]]
        secondPoint = [xCor[i+1], yCor[i+1]]
        tempDistacne = math.sqrt(math.pow((firstPoint[0] - secondPoint[0]), 2) +
                                 math.pow((firstPoint[1] - secondPoint[1]), 2))
        if (pointsCount <= 0) :
            break
        distanceArray.append(tempDistacne)
    # Data for plotting
    speedOfEyes = []  #  In km/s
    pointPerMilliSecond = 1 / deltaTimePerPoint
    time = np.arange(0.0, timeOfRound, pointPerMilliSecond)
    for i in range (len(distanceArray)):
        speedOfEyes.append(float(distanceArray[i] / pointPerMilliSecond))
    fig, ax = plt.subplots()
    #  check the size of time
    if time.__len__() > speedOfEyes.__len__():
        time = time[1:]
    plt.plot(time, speedOfEyes, linestyle='solid', color='blue')
    plt.show()
def CreateCardBoard(listOfImage):
    print('The board creation is in process...')
    path = 'allcards/'  # get the path of images
    imageList = []
    for i in range(12):
        imageList.append(listOfImage[str(i)]+'.png')
    pdf = FPDF('L', 'mm', 'A4')  # create an A4-size pdf document
    pdf.add_page()
    x, y, w, h = 0, 52.07, 47.6, 25.7
    i = 0
    for image in imageList:
        if (x == 191.39999999999998):
            x = 63.8
            y = y + 25.9
        else:
            x = x + 63.8
        pdf.image(path + image, x, y, w, h)
    pdf.output("tempCardBoard.pdf", "F")
    print('The board creation is in finished ...')
def CreateDominantCardBoard(listOfCardByRound):
    #  The GaussianBlur() uses the Gaussian kernel.
    #  The height and width of the kernel should be a positive and an odd number.
    #  Then you have to specify the X and Y direction that is sigmaX and sigmaY respectively.
    #  If only one is specified, both are considered the same.
    creationFlag = False
    if listOfCardByRound == False:
        print('Sorry the round has no dominant value')
        return False
    print('The dominant board creation is in process...')
    path = 'allcards/'  # get the path of images
    tempPath = 'tempcardboard/'
    imageListHighlight = []
    imageList = []
    #  Get the card list of dominant value from board
    for i in range(listOfCardByRound.__len__()):
        imageListHighlight.append(listOfCardByRound[i]+'.png')
    #  Get the all board list
    listOfCardByRound = db.GetBoard('Gulkin', 3)
    for i in range(12):
        imageList.append(listOfCardByRound[str(i)] + '.png')
    #Create New Board with highlight cards
    for i in range(12):
        for j in range(imageListHighlight.__len__()):
            if imageList[i] == imageListHighlight[j]:
             img = cv2.imread(path + imageListHighlight[j])
             cv2.imwrite(tempPath + imageListHighlight[j], img)
             creationFlag = True
             break
        if creationFlag == False:
            img = cv2.imread(path + imageList[i])
            blur_image = cv2.GaussianBlur(img, (61, 61), 0)
            cv2.imwrite(tempPath + imageList[i], blur_image)
        creationFlag = False
    pdf = FPDF('L', 'mm', 'A4')  # create an A4-size pdf document
    pdf.add_page()
    x, y, w, h = 0, 52.07, 47.6, 25.7
    for image in imageList:
        if (x == 191.39999999999998):
            x = 63.8
            y = y + 25.9
        else:
            x = x + 63.8
        pdf.image(tempPath + image, x, y, w, h)
    pdf.output("tempCardHighlightBoard.pdf", "F")
    print('The dominant board creation is in finished ...')
def PDF2Image():
    # To user this function u must install Popper and put the path into System Path
    # You can use https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows
    images = convert_from_path('tempCardBoard.pdf', 500)
    for page in images:
        page.save('out.jpg', 'JPEG')
def plt2PDF(fig):
    try:
        fig.savefig("testPlot.pdf", bbox_inches='tight')
    except:
        print('Error please close the Testplot.pdf and try again')
    return
def GetAvgSpeedOfSpeedUpEyes(speedOfEyes):
    return sum(speedOfEyes) / len(speedOfEyes)
Main()
#Yaniv Change