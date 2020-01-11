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
def Main():
    print()
    # print(db.GetNumberOfRoundByUsername('mnb'))
    # print('Please enter your userName')
    # db.DominatValue('Yaniv', 21)
    #HeatMapFunction('Gulkin', 14, 0)
    # print(db.GetCoordinateByRoundNumber('Gulkin', 1))
    # PointDrawing('Gulkin', 10, 0)
    SpeedUpEyes('Gulkin', 17)
    # CreateCardBoard(db.GetBoard('mnb', 232))
    # PDF2Image()
    # CreateDominantCardBoard()
# MyPlot function helps to maps all the point into gaussian numbers
def myplot(x, y, s, bins=1000):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent
def PointDrawing(userName, userRound, dominateFlag):
    removeFlag = 0
    saveLastPointX = 0
    saveLastPointY = 0
    i = 0
    print("STARTING TO CREATE POINT DRAWING GRAPH")
    if (dominateFlag == 0):
        print("REGULAR BOARD HAS BEEN SELECTED TO BE CREATED")
        listOfCardByRound = db.GetBoard(userName, int(userRound))
        CreateCardBoard(listOfCardByRound)
    if (dominateFlag == 1):
        print("DOMINATE BOARD HAS BEEN  SELECTED TO BE CREATED")
        listOfCardByRound = db.DominatValue(userName, int(userRound))
        CreateDominantCardBoard(listOfCardByRound, userName, userRound)
    PDF2Image()
    listOfCoodinate = db.GetCoordinateByRoundNumber(userName, userRound)
    xCor = []
    yCor = []
    for x in listOfCoodinate[0]:
        x = float(x)
        #  Calibrate the camera in x axis for the image
        x += 140
        if x < 450 or x > 1650:
            xCor.append(-190.0)
        #  Yaniv think that is should be 300
        elif x > saveLastPointX + 310 or x < saveLastPointX - 310:
            saveLastPointX = x
            xCor.append(x)
        else:
            xCor.append(-190.0)
    for y in listOfCoodinate[1]:
        y = float(y)
        #  Calibrate the camera in y axis for the image
        y -= 200
        if y > 755 or y < 200:
            yCor.append(-190.0)
        elif y > saveLastPointY + 130 or y < saveLastPointY - 130:
            saveLastPointX = y
            yCor.append(y)
        else:
            yCor.append(-190.0)
    #  Remove all unnecessary points
    while removeFlag == 0:
        try:
            if xCor[i] == -190.0 or yCor[i] == -190.0:
                del xCor[i]
                del yCor[i]
            else:
                i += 1
        except:
            print("Finish to remove unnecessary points")
            removeFlag = 1
    map_img = mpimg.imread('out.jpg')
    try:
        plt.plot(xCor, yCor, 'o-', color='blue')
        plt.plot(xCor[0], yCor[0], 'o-', color='red')
    except:
        print('Sorry But this graph are not available because all points are too close.')
        return
    plt.imshow(map_img, zorder=0, extent=[0, 2006, 960, 0], aspect='auto')
    plt2PDF(plt)
    webbrowser.open_new(r'testPlot.pdf')
    plt.show()
def HeatMapFunction(username, roundNumber, dominateFlag):
    #  Connect to DB and create a Board
    if(dominateFlag==0):
      print("REGULAR BOARD HAS BEEN SELECTED TO BE CREATED")
      listOfCardByRound = db.GetBoard(username, int(roundNumber))
      CreateCardBoard(listOfCardByRound)
    if (dominateFlag == 1):
      print("DOMINATE BOARD HAS BEEN  SELECTED TO BE CREATED")
      listOfCardByRound = db.DominatValue(username, int(roundNumber))
      CreateDominantCardBoard(listOfCardByRound, username, int(roundNumber))
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
    pointPerMilliSecond = (timeOfRound / pointsCount)
    time = np.arange(0.0, timeOfRound, pointPerMilliSecond)
    for i in range(len(distanceArray)):
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
def CreateDominantCardBoard(listOfCardByRound, username, roundNumber):
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
    listOfCardByRound = db.GetBoard(username, roundNumber)
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
            blur_image = cv2.GaussianBlur(img, (81, 81), 0)
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
    pdf.output("tempCardBoard.pdf", "F")
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