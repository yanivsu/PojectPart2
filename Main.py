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
    HeatMapFunction('Gulkin', 12, 0, 0)
    # print(db.GetCoordinateByRoundNumber('Gulkin', 1))
    # PointDrawing('user1', 7, 0)
    # durationTimeOnCard('user1', 7)
    # SpeedUpEyes('user4', 7)
    # CreateCardBoard(db.GetBoard('mnb', 232))
    # PDF2Image()
    # CreateDominantCardBoard()
# MyPlot function helps to maps all the point into gaussian numbers
def getNMaxElements(durationTimeList, N):
     final_list = []
     for i in range(0, N):
         max1 = 0
         for j in range(len(durationTimeList)):
            if durationTimeList[j] > max1:
             max1 = durationTimeList[j]
         durationTimeList.remove(max1)
         final_list.append(max1)
     return final_list
def durationTimeOnCard(userName, userRound):
    durationTimeList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    maxNValues = []
    listOfCoodinate = db.GetCoordinateByRoundNumber(userName, int(userRound))
    xCor = listOfCoodinate[0]
    yCor = listOfCoodinate[1]
    for i in range(len(xCor)):
        xCor[i] = float(xCor[i])
    for i in range(len(yCor)):
        yCor[i] = float(yCor[i])
    roundTime = db.GetTimeDeatilsPerRound(userName, userRound)
    durationTimeList = getEyesOnCardsData(xCor, yCor, roundTime[1])
    # maxNValues = getNMaxElements(durationTimeList, 5)
    maxNValues = GetMaxIndices(durationTimeList)
    createBarChart(maxNValues, durationTimeList, roundTime[1], userName)
    createPieChart(maxNValues, durationTimeList, roundTime[1], userName)
def getAnalysis(userName, roundNumber, analysisFlag):
    print()
    durationTimeOnCard()
def createPieChart(maxNValues, durationTimeList, roundTime, userName):
    names = (maxNValues[0] + 1, maxNValues[1] + 1, maxNValues[2] + 1, maxNValues[3] + 1, maxNValues[4] + 1)
    scores = [durationTimeList[maxNValues[0]], durationTimeList[maxNValues[1]], durationTimeList[maxNValues[2]],
              durationTimeList[maxNValues[3]], durationTimeList[maxNValues[4]]]
    plt.axis("equal")
    plt.pie(scores, labels=names, autopct="%0.2f%%")
    plt.title('PieChart ' + userName)
    plt2PDFPie(plt)
    webbrowser.open_new(r'testPlotPie.pdf')
    plt.show()
def createBarChart(maxNValues, durationTimeList, roundTime, userName):
    fig = plt.figure(figsize=(7, 5))
    names = (maxNValues[0] + 1, maxNValues[1] + 1, maxNValues[2] + 1, maxNValues[3] + 1, maxNValues[4] + 1)
    scores = [durationTimeList[maxNValues[0]], durationTimeList[maxNValues[1]], durationTimeList[maxNValues[2]],
              durationTimeList[maxNValues[3]], durationTimeList[maxNValues[4]]]
    position = [0, 1, 2, 3, 4]
    plt.grid()
    plt.ylim(0, roundTime)
    plt.xticks(position, names)
    plt.bar(position, scores, width=0.3)
    plt.title("Gaze duration on cards")
    plt.xlabel("Cards")
    plt.ylabel("Time(sec)")
    plt.title('Bar Char ' + userName)
    plt2PDFBar(plt)
    webbrowser.open_new(r'testPlotBarChar.pdf')
    plt.show()
def getEyesOnCardsData(xCor, yCor, roundTime):
    durationTimeList=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    deltaTime = (roundTime / len(xCor))
    for i in range(len(xCor)):
        # ---------------- FIRST ROW ----------------#
        ####### Card Number 1 #######
        if (xCor[i] > 400.0 and xCor[i] < 760.0 and yCor[i] > 410.0 and yCor[i] < 530.0):
            durationTimeList[0] = durationTimeList[0] + deltaTime
            ####### Card Number 2 #######
        if (xCor[i] > 860.0 and xCor[i] < 1200.0 and yCor[i] > 410.0 and yCor[i] < 530.0):
            durationTimeList[1] = durationTimeList[1] + deltaTime
        ####### Card Number 3 #######
        if (xCor[i] > 1300.0 and xCor[i] < 1600.0 and yCor[i] > 410.0 and yCor[i] < 530.0):
            durationTimeList[2] = durationTimeList[2] + deltaTime
        # ---------------- SECOND ROW ----------------#
        ####### Card Number 4 #######
        if (xCor[i] > 400.0 and xCor[i] < 750.0 and yCor[i] > 560.0 and yCor[i] < 660.0):
            durationTimeList[3] = durationTimeList[3] + deltaTime
            ####### Card Number 5 #######
        if (xCor[i] > 875.0 and xCor[i] < 1200.0 and yCor[i] > 560.0 and yCor[i] < 660.0):
            durationTimeList[4] = durationTimeList[4] + deltaTime
            ####### Card Number 6 #######
        if (xCor[i] > 1300.0 and xCor[i] < 1600.0 and yCor[i] > 560.0 and yCor[i] < 660.0):
            durationTimeList[5] = durationTimeList[5] + deltaTime
        # ---------------- THIRD ROW ----------------#
        ####### Card Number 7 #######
        if (xCor[i] > 400.0 and xCor[i] < 750 and yCor[i] > 670.0 and yCor[i] < 770.0):
            durationTimeList[6] = durationTimeList[6] + deltaTime
            ####### Card Number 8 #######
        if (xCor[i] > 900 and xCor[i] < 1200 and yCor[i] > 670.0 and yCor[i] < 770.0):
            durationTimeList[7] = durationTimeList[7] + deltaTime
            ####### Card Number 9 #######
        if (xCor[i] > 1300 and xCor[i] < 1600 and yCor[i] > 670.0 and yCor[i] < 770.0):
            durationTimeList[8] = durationTimeList[8] + deltaTime
        # ---------------- FOURTH ROW ----------------#
        ####### Card Number 10 #######
        if (xCor[i] > 425 and xCor[i] < 725 and yCor[i] > 780 and yCor[i] < 880):
            durationTimeList[9] = durationTimeList[9] + deltaTime
            ####### Card Number 11 #######
        if (xCor[i] > 900 and xCor[i] < 1200 and yCor[i] > 780 and yCor[i] < 880):
            durationTimeList[10] = durationTimeList[10] + deltaTime
            ####### Card Number 12 #######
        if (xCor[i] > 1325 and xCor[i] < 1625 and yCor[i] > 780 and yCor[i] < 880):
            durationTimeList[11] = durationTimeList[11] + deltaTime
    return durationTimeList
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
        listOfCardByRound = db.DominatValue(userName, int(userRound))[0]
        CreateDominantCardBoard(listOfCardByRound, userName, userRound)
    PDF2Image()
    listOfCoodinate = db.GetCoordinateByRoundNumber(userName, userRound)
    roundTime = db.GetTimeDeatilsPerRound(userName, userRound)
    xCor = []
    yCor = []
    for x in listOfCoodinate[0]:
        x = float(x)
        if x < 580 or x > 1650:
            xCor.append(-190.0)
        elif x > saveLastPointX + 200 or x < saveLastPointX - 200:
            saveLastPointX = x
            x *= 1.8
            x -= 660
            xCor.append(x)
        else:
            xCor.append(-190.0)
    for y in listOfCoodinate[1]:
        y = float(y)
        if y > 900 or y < 300:
            yCor.append(-190.0)
        elif y > saveLastPointY or y < saveLastPointY :
            saveLastPointX = y
            yCor.append(y - 150)
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
        plt.title('Point Drawing Map ' + userName)
        plt.text(5, 100, "Round Time: " + roundTime[1].__str__())
        plt.text(5, 135, "Fast Movements: " + xCor.__len__().__str__())
        plt.plot(xCor[0], yCor[0], 'o-', color='red')
    except:
        print('Sorry But this graph are not available because all points are too close.')
        return
    plt.imshow(map_img, zorder=0, extent=[0, 2006, 960, 0], aspect='auto')
    plt2PDF(plt)
    webbrowser.open_new(r'testPlot.pdf')
    plt.show()
def HeatMapFunction(username, roundNumber, dominateFlag, analysisFlag):
    #  Connect to DB and create a Board
    if dominateFlag == 0:
      print("REGULAR BOARD HAS BEEN SELECTED TO BE CREATED")
      listOfCardByRound = db.GetBoard(username, int(roundNumber))
      CreateCardBoard(listOfCardByRound)
    if dominateFlag == 1:
      print("DOMINATE BOARD HAS BEEN  SELECTED TO BE CREATED")
      listOfCardByRound = db.DominatValue(username, int(roundNumber))[0]
      CreateDominantCardBoard(listOfCardByRound, username, int(roundNumber))
    PDF2Image()
    listOfCoodinate = db.GetCoordinateByRoundNumber(username, int(roundNumber))
    xCor = []
    yCor = []
    #  Convert String point to float point
    for x in listOfCoodinate[0]:
        x = float(x)
        #  Calibrate the camera x axis for the image
        x *= 1.5
        x -= 340
        xCor.append(float(x))
    for y in listOfCoodinate[1]:
        y = float(y)
        #  Calibrate the camera y axis for the image
        y -= 120
        yCor.append(float(y))
    plt.subplots(figsize=(12, 12))
    map_img = mpimg.imread('out.jpg')
    hmax = sns.kdeplot(xCor, yCor, cmap="Blues", shade=False)
    hmax.collections[0].set_alpha(0)
    #  Extent helps me to set the axis 0 =>2006 in
    # X axis and 960 => 0 in y axis
    plt.title('HeatMap ' + username)
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
    speedOfEyes = []
    pointPerMilliSecond = (timeOfRound / pointsCount)
    time = np.arange(0.0, timeOfRound, pointPerMilliSecond)
    for i in range(len(distanceArray)):
        speedOfEyes.append(float(distanceArray[i] / pointPerMilliSecond)*0.01)
    fig, ax = plt.subplots()
    #  check the size of time
    if time.__len__() > speedOfEyes.__len__():
        time = time[1:]
    #  Get Max of speed
    maxSpeed = max(speedOfEyes).__round__(2)
    avgSpeed = GetAvgSpeedOfSpeedUpEyes(speedOfEyes=speedOfEyes).__round__(2)
    varOfSpeed = np.var(speedOfEyes).__round__(2)
    plt.title('Speed of eye ' + userName)
    plt.xlabel('Time[Sec]')
    plt.ylabel('Km/h')
    str1 = "Max Speed is:"+maxSpeed.__str__()
    str2 = "Avg Speed is:"+avgSpeed.__str__()
    str3 = "Variance speed is:"+varOfSpeed.__str__()
    plt.text(80, 80, str1, fontsize=14)
    plt.text(80, 150, str2, fontsize=14)
    plt.text(80, 220, str3, fontsize=14)
    plt.plot(time, speedOfEyes, linestyle='solid', color='blue')
    plt2PDF(plt)
    webbrowser.open_new(r'testPlot.pdf')
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
        if x == 191.39999999999998:
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
def plt2PDFPie(fig):
    try:
        fig.savefig("testPlotPie.pdf", bbox_inches='tight')
    except:
        print('Error please close the Testplot.pdf and try again')
    return
def plt2PDFBar(fig):
    try:
        fig.savefig("testPlotBarChar.pdf", bbox_inches='tight')
    except:
        print('Error please close the Testplot.pdf and try again')
    return
def GetAvgSpeedOfSpeedUpEyes(speedOfEyes):
    return sum(speedOfEyes) / len(speedOfEyes)
def GetMaxIndices(array):
    indicesArray = np.argpartition(array, -5)[-5:]
    indicesArray = np.sort(indicesArray)
    return indicesArray
Main()