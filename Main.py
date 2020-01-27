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
from KMedoids import KMedoids

#  To run this code you should install all the lib to python and install poppler lib
# You can use https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows

def Main():
    print()
    # print(db.GetNumberOfRoundByUsername('mnb'))
    # print('Please enter your userName')
    # db.DominatValue('Yaniv', 21)
    # HeatMapFunction('user1', 7, 0, 0)
    # print(db.GetCoordinateByRoundNumber('Gulkin', 1))
    # PointDrawing('user5', 7, 0, 0)
    # durationTimeOnCard('user1', 8)
    # SpeedUpEyes('user5', 7, 0)
    # CreateCardBoard(db.GetBoard('mnb', 232))
    # PDF2Image()
    # CreateDominantCardBoard()
    # CalusterValuesByPam()
    # users = ['user1', 'user2', 'user4', 'user5', 'user7', 'user8', 'user11']
    # ClusterDataBySpeedVar(users)
    # ClusterDataBySpeedAndFastMovmentAVG(users)
    # ClusterDataBySpeedFastMovments(users)
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
def GetHeatMapFeatures(userName, userRound,cardIndexList,domFlag):
    durationTimeList = []
    listOfCoodinate = db.GetCoordinateByRoundNumber(userName, int(userRound))
    xCor = listOfCoodinate[0]
    yCor = listOfCoodinate[1]
    for i in range(len(xCor)):
        xCor[i] = float(xCor[i])
    for i in range(len(yCor)):
        yCor[i] = float(yCor[i])
    roundTime = db.GetTimeDeatilsPerRound(userName, userRound)
    durationTimeList = getEyesOnCardsData(xCor, yCor, roundTime[1])
    if domFlag == 1:
     domList0=[]
     domList1=[]
     domList2=[]
     temp=[]
     for i in range(len(cardIndexList)):
          temp = durationTimeList[0]
          domList0.append(temp[cardIndexList[i]-1])
          temp = durationTimeList[1]
          domList1.append(temp[cardIndexList[i]-1])
          temp = durationTimeList[2]
          domList2.append(temp[cardIndexList[i]-1])
     maxNValues = GetMaxIndices(domList0, domFlag)
     maxNValues2 = GetMaxIndices(domList2, domFlag)
     createDomDurationBarChart(maxNValues, domList0, roundTime[1], userName,cardIndexList)
     createDomLookAtCardBarChart(maxNValues, domList1, roundTime[1], userName, cardIndexList)
     createDomAveragePieChart(maxNValues2, domList2, roundTime[1], userName, durationTimeList[3], cardIndexList)
    if domFlag==0:
     # maxNValues = getNMaxElements(durationTimeList, 5)
     maxNValues = GetMaxIndices(durationTimeList[0],domFlag)
     maxNValues2=GetMaxIndices(durationTimeList[2],domFlag)
     createDurationBarChart(maxNValues, durationTimeList[0], roundTime[1], userName)
     createLookAtCardBarChart(maxNValues, durationTimeList[1], roundTime[1], userName)
     createAveragePieChart(maxNValues2, durationTimeList[2], roundTime[1], userName,durationTimeList[3])
def createAveragePieChart(maxNValues, durationTimeList, roundTime, userName, varAvg):
         score = []
         cards = []
         objects = [maxNValues[0] + 1, maxNValues[1] + 1, maxNValues[2] + 1, maxNValues[3] + 1,
                    maxNValues[4] + 1]  # X cor
         y_pos = np.arange(len(objects))
         performance = [durationTimeList[maxNValues[0]], durationTimeList[maxNValues[1]],
                        durationTimeList[maxNValues[2]],
                        durationTimeList[maxNValues[3]], durationTimeList[maxNValues[4]]]

         for i in range(len(maxNValues)):
             if performance[i] > 0.01:
                 score.append(performance[i])
                 cards.append(maxNValues[i] + 1)
         totalVal = sum(score)
         returnValue = CheckIfNot100Presents(totalVal)
         if returnValue[0] == True:
             cards.append("REST OF CARDS")
             score.append(returnValue[1])
         plt.axis("equal")
         str1 = "Variance speed is:" + varAvg
         # plt.text(80, 80, str1, fontsize=14)
         plt.pie(score, labels=cards, autopct="%0.2f%%")
         plt.title(userName + " - gaze distribution by percentage")
         plt2PDFBar(plt, "AVG", userName)
         webbrowser.open_new(r'AVG_' + userName + '.pdf')
         plt.show()
def createLookAtCardBarChart(maxNValues, durationTimeList, roundTime, userName):
         objects = ('1', '2', '3', '4',
                    '5', '6', '7', '8',
                    '9', '10', '11', '12',)  # X cor
         y_pos = np.arange(len(objects))
         performance = durationTimeList  # Y cor
         plt.grid()
         plt.bar(y_pos, performance, align='center', alpha=0.5)
         plt.xticks(y_pos, objects)
         plt.title(userName + " - look at card counter")
         plt.xlabel("Cards")
         plt.ylabel("Counter")
         plt2PDFBar(plt, "LOOK", userName)
         webbrowser.open_new(r'LOOK_' + userName + '.pdf')
         plt.show()
def createDomDurationBarChart(maxNValues, durationTimeList, roundTime, userName, cardIndexList):
         names = []
         scores = []
         position = []
         for i in range(len(maxNValues)):
             names.append(cardIndexList[i])
             position.append(i)
             scores.append(durationTimeList[maxNValues[i]])
         plt.grid()
         plt.ylim(0, sum(durationTimeList))
         plt.xticks(position, names)
         plt.bar(position, scores, width=0.3)
         plt.title(userName + " - gaze duration on  dominant cards by sec")
         plt.xlabel("Cards number")
         plt.ylabel("Time(sec)")
         plt2PDFBar(plt, "DOM DUR", userName)
         webbrowser.open_new(r'DOM DUR_' + userName + '.pdf')
         plt.show()
def createDomLookAtCardBarChart(maxNValues, durationTimeList, roundTime, userName, cardIndexList):
         names = []
         scores = []
         position = []
         for i in range(len(maxNValues)):
             names.append(cardIndexList[i])
             position.append(i)
             scores.append(durationTimeList[maxNValues[i]])
         plt.grid()
         plt.ylim(0, sum(durationTimeList))
         plt.xticks(position, names)
         plt.bar(position, scores, width=0.3)
         plt.title(userName + " - look at dominant card counter")
         plt.xlabel("Cards")
         plt.ylabel("Counter")
         plt2PDFBar(plt, "DOM LOOK", userName)
         webbrowser.open_new(r'DOM LOOK_' + userName + '.pdf')
         plt.show()
         #########################maxNValues2, domList2, roundTime[1], userName, durationTimeList[3], cardIndexList
def createDomAveragePieChart(maxNValues, durationTimeList, roundTime, userName, varAvg, cardIndexList):
         objects = []
         score = []
         cards = []
         performance = []
         for i in range(len(maxNValues)):
             objects.append(cardIndexList[i])
             performance.append(durationTimeList[i])
         for i in range(len(maxNValues)):
             if performance[i] > 0.01:
                 score.append(performance[i])
                 cards.append(cardIndexList[i] + 1)

         totalVal = sum(score)
         returnValue = CheckIfNot100Presents(totalVal)
         if returnValue[0] == True:
             cards.append("NONE DOMINANTE CARDS")
             score.append(returnValue[1])

         plt.axis("equal")
         # str1 = "Variance speed is:" + varAvg
         # plt.text(80, 80, str1, fontsize=14)
         plt.pie(score, labels=cards, autopct="%0.2f%%")
         plt.title(userName + " - gaze distribution on dominant cards by percentage")
         plt2PDFBar(plt, "DOM AVG", userName)
         webbrowser.open_new(r'DOM AVG_' + userName + '.pdf')
         plt.show()
def createDurationBarChart(maxNValues, durationTimeList, roundTime, userName):
         names = (maxNValues[0] + 1, maxNValues[1] + 1, maxNValues[2] + 1, maxNValues[3] + 1, maxNValues[4] + 1)
         scores = [durationTimeList[maxNValues[0]], durationTimeList[maxNValues[1]], durationTimeList[maxNValues[2]],
                   durationTimeList[maxNValues[3]], durationTimeList[maxNValues[4]]]
         position = [0, 1, 2, 3, 4]
         plt.grid()
         plt.ylim(0, sum(maxNValues))
         plt.xticks(position, names)
         plt.bar(position, scores, width=0.3)
         plt.title(userName + " - gaze duration on cards by sec")
         plt.xlabel("Cards number")
         plt.ylabel("Time(sec)")
         plt2PDFBar(plt, "DUR", userName)
         webbrowser.open_new(r'DUR_' + userName + '.pdf')
         plt.show()
def CheckIfNot100Presents(totalVal):
         if totalVal < 1:
             diff = 1 - totalVal
             flag = True
         return flag, diff
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
def createAverageBarChart(maxNValues, durationTimeList, roundTime, userName):
    objects = ('1', '2', '3', '4',
               '5', '6', '7', '8',
               '9', '10', '11', '12',)  # X cor
    y_pos = np.arange(len(objects))
    performance = durationTimeList  # Y cor
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.title("Gaze duration on cards")
    plt.xlabel("Cards")
    plt.ylabel("Time(sec)")
    plt.title('Bar Char ' + userName)
    plt2PDFBar(plt, "AVG")
    webbrowser.open_new(r'Average eye duration on card.pdf')
    plt.show()
def getEyesOnCardsData(xCor, yCor, roundTime):
        deltaTime = (roundTime / len(xCor))
        durationTimeList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        lookAtCardCounter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        avgTimeOnCard = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for i in range(len(xCor)):
            xCor[i] *= 1.5
            xCor[i] -= 340
            yCor[i] -= 120
            # ---------------- FIRST ROW ----------------#
            ####### Card Number 1 #######
            if (xCor[i] > 400.0 and xCor[i] < 760.0 and yCor[i] > 410.0 and yCor[i] < 530.0):
                durationTimeList[0] = durationTimeList[0] + deltaTime
                lookAtCardCounter[0] = lookAtCardCounter[0] + 1
                ####### Card Number 2 #######
            if (xCor[i] > 860.0 and xCor[i] < 1200.0 and yCor[i] > 410.0 and yCor[i] < 530.0):
                durationTimeList[1] = durationTimeList[1] + deltaTime
                lookAtCardCounter[1] = lookAtCardCounter[1] + 1
            ####### Card Number 3 #######
            if (xCor[i] > 1300.0 and xCor[i] < 1600.0 and yCor[i] > 410.0 and yCor[i] < 530.0):
                durationTimeList[2] = durationTimeList[2] + deltaTime
                lookAtCardCounter[2] = lookAtCardCounter[2] + 1
            # ---------------- SECOND ROW ----------------#
            ####### Card Number 4 #######
            if (xCor[i] > 400.0 and xCor[i] < 750.0 and yCor[i] > 560.0 and yCor[i] < 660.0):
                durationTimeList[3] = durationTimeList[3] + deltaTime
                lookAtCardCounter[3] = lookAtCardCounter[3] + 1
                ####### Card Number 5 #######
            if (xCor[i] > 875.0 and xCor[i] < 1200.0 and yCor[i] > 560.0 and yCor[i] < 660.0):
                durationTimeList[4] = durationTimeList[4] + deltaTime
                lookAtCardCounter[4] = lookAtCardCounter[4] + 1
                ####### Card Number 6 #######
            if (xCor[i] > 1300.0 and xCor[i] < 1600.0 and yCor[i] > 560.0 and yCor[i] < 660.0):
                durationTimeList[5] = durationTimeList[5] + deltaTime
                lookAtCardCounter[5] = lookAtCardCounter[5] + 1
            # ---------------- THIRD ROW ----------------#
            ####### Card Number 7 #######
            if (xCor[i] > 400.0 and xCor[i] < 750 and yCor[i] > 670.0 and yCor[i] < 770.0):
                durationTimeList[6] = durationTimeList[6] + deltaTime
                lookAtCardCounter[6] = lookAtCardCounter[6] + 1
                ####### Card Number 8 #######
            if (xCor[i] > 900 and xCor[i] < 1200 and yCor[i] > 670.0 and yCor[i] < 770.0):
                durationTimeList[7] = durationTimeList[7] + deltaTime
                lookAtCardCounter[7] = lookAtCardCounter[7] + 1
                ####### Card Number 9 #######
            if (xCor[i] > 1300 and xCor[i] < 1600 and yCor[i] > 670.0 and yCor[i] < 770.0):
                durationTimeList[8] = durationTimeList[8] + deltaTime
                lookAtCardCounter[8] = lookAtCardCounter[8] + 1
            # ---------------- FOURTH ROW ----------------#
            ####### Card Number 10 #######
            if (xCor[i] > 425 and xCor[i] < 725 and yCor[i] > 780 and yCor[i] < 880):
                durationTimeList[9] = durationTimeList[9] + deltaTime
                lookAtCardCounter[9] = lookAtCardCounter[9] + 1
                ####### Card Number 11 #######
            if (xCor[i] > 900 and xCor[i] < 1200 and yCor[i] > 780 and yCor[i] < 880):
                durationTimeList[10] = durationTimeList[10] + deltaTime
                lookAtCardCounter[10] = lookAtCardCounter[10] + 1
                ####### Card Number 12 #######
            if (xCor[i] > 1325 and xCor[i] < 1625 and yCor[i] > 780 and yCor[i] < 880):
                durationTimeList[11] = durationTimeList[11] + deltaTime
                lookAtCardCounter[11] = lookAtCardCounter[11] + 1
        for counter in range(len(avgTimeOnCard)):
            avgTimeOnCard[counter] = (lookAtCardCounter[counter] * deltaTime) / sum(durationTimeList)

        varAVG = np.var(avgTimeOnCard).__str__()
        return durationTimeList, lookAtCardCounter, avgTimeOnCard, varAVG
def myplot(x, y, s, bins=1000):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent
def PointDrawing(userName, userRound, dominateFlag, cluster):
    removeFlag = 0
    saveLastPointX = 0
    saveLastPointY = 0
    i = 0
    print("STARTING TO CREATE POINT DRAWING GRAPH")
    if cluster == 0:
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
        elif y > saveLastPointY or y < saveLastPointY:
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
    if cluster == 1:
        return xCor.__len__()
    try:
        plt.plot(xCor, yCor, 'o-', color='blue')
        plt.title('Point Drawing Map ' + userName)
        plt.text(5, 100, "Round Time: " + roundTime[1].__str__())
        plt.text(5, 135, "Number of transicion between cards: " + xCor.__len__().__str__())
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
        cardIndexList = []
        if dominateFlag == 0:
            print("REGULAR BOARD HAS BEEN SELECTED TO BE CREATED")
            listOfCardByRound = db.GetBoard(username, int(roundNumber))
            CreateCardBoard(listOfCardByRound)
        if dominateFlag == 1:
            print("DOMINATE BOARD HAS BEEN  SELECTED TO BE CREATED")
            listOfCardByRound = db.DominatValue(username, int(roundNumber))[0]
            cardIndexList = db.DominatValue(username, int(roundNumber))[1]
            CreateDominantCardBoard(listOfCardByRound, username, int(roundNumber))

        GetHeatMapFeatures(username, roundNumber, cardIndexList, dominateFlag)
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
            y -= 210
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
def SpeedUpEyes(userName, userRound, cluster):
    print("STARTING TO CREATE SPEED EYE GRAPH")
    listOfCoodinate = db.GetCoordinateByRoundNumber(userName, userRound)
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
    # Calcuate Distance
    distanceArray = []
    for i in range(len(xCor) - 1):
        firstPoint = [xCor[i], yCor[i]]
        secondPoint = [xCor[i + 1], yCor[i + 1]]
        tempDistacne = math.sqrt(math.pow((firstPoint[0]/5.797 - secondPoint[0]/5.797), 2) +
                                 math.pow((firstPoint[1]/5.797 - secondPoint[1]/5.797), 2))
        if (pointsCount <= 0):
            break
        if tempDistacne > 100:
            print('Noise')
            pointsCount -= 1
        else:
            distanceArray.append(tempDistacne)
    # Data for plotting
    speedOfEyes = []
    pointPerMilliSecond = (timeOfRound / pointsCount)
    time = np.arange(0.0, timeOfRound, pointPerMilliSecond)
    for i in range(len(distanceArray)):
        speedOfEyes.append(float(distanceArray[i] / pointPerMilliSecond)*0.01)
    if cluster == 0:
        fig, ax = plt.subplots()
    #  check the size of time
    if time.__len__() > speedOfEyes.__len__():
        time = time[1:]
    #  Get Max of speed
    maxSpeed = max(speedOfEyes).__round__(2)
    avgSpeed = GetAvgSpeedOfSpeedUpEyes(speedOfEyes=speedOfEyes).__round__(2)
    varOfSpeed = np.var(speedOfEyes).__round__(2)
    if cluster == 1:
        print('Round Finish!')
        return varOfSpeed
    str1 = "Max Speed is:" + maxSpeed.__str__()
    str2 = "Avg Speed is:" + avgSpeed.__str__()
    str3 = "Variance speed is:" + varOfSpeed.__str__()
    fig, (ax1, ax2) = plt.subplots(2, 1, constrained_layout=True)
    ax1.plot(time, speedOfEyes, linestyle='solid', color='blue')
    ax1.set_title('Speed of eye ' + userName)
    ax1.set_xlabel('Time [Sec]')
    ax1.set_ylabel('Distance (mm)')
    ax2.text(0, .0, str1)
    ax2.text(0, .02, str2)
    ax2.text(0, .04, str3)
    ax2.plot([0, 0], [0, 0])
    ax2.axis('off')
    plt2PDF(fig)
    webbrowser.open_new(r'testPlot.pdf')
    plt.show()
def CreateCardBoard(listOfImage):
    print('The board creation is in process...')
    path = 'allcards/'  # get the path of images
    imageList = []
    for i in range(12):
        imageList.append(listOfImage[str(i)] + '.png')
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
        imageListHighlight.append(listOfCardByRound[i] + '.png')
    #  Get the all board list
    listOfCardByRound = db.GetBoard(username, roundNumber)
    for i in range(12):
        imageList.append(listOfCardByRound[str(i)] + '.png')
    # Create New Board with highlight cards
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
def plt2PDFBar(fig, type,userName):
    if type == "DUR":
        try:
            fig.savefig(type+"_"+userName+".pdf", bbox_inches='tight')
        except:
            print('Error please close the Testplot.pdf and try again')
    if type == "LOOK":
        try:
            fig.savefig(type+"_"+userName+".pdf", bbox_inches='tight')
        except:
            print('Error please close the Testplot.pdf and try again')
    if type == "AVG":
        try:
            fig.savefig(type+"_"+userName+".pdf", bbox_inches='tight')
        except:
            print('Error please close the Testplot.pdf and try again')
    if type == "DOM DUR":
        try:
            fig.savefig(type+"_"+userName+".pdf", bbox_inches='tight')
        except:
            print('Error please close the Testplot.pdf and try again')
    if type == "DOM LOOK":
        try:
            fig.savefig(type+"_"+userName+".pdf", bbox_inches='tight')
        except:
            print('Error please close the Testplot.pdf and try again')
    if type == "DOM AVG":
        try:
            fig.savefig(type+"_"+userName+".pdf", bbox_inches='tight')
        except:
            print('Error please close the Testplot.pdf and try again')
    return
def plt2PDFClusterByOneValue(fig):
    try:
        fig.savefig("ClusterByOneValue.pdf", bbox_inches='tight')
    except:
        print('Error please close the Testplot.pdf and try again')
    return
def plt2PDFClusterByTwoValues(fig):
    try:
        fig.savefig("ClusterByTwoValues.pdf", bbox_inches='tight')
    except:
        print('Error please close the Testplot.pdf and try again')
    return
def GetAvgSpeedOfSpeedUpEyes(speedOfEyes):
    return sum(speedOfEyes) / len(speedOfEyes)
def GetMaxIndices(array,domFlag):
    if domFlag==0:
        indicesArray = np.argpartition(array, -5)[-5:]
        indicesArray = np.sort(indicesArray)
    if domFlag==1:
        indicesArray = np.argpartition(array, 0)[0:]
        indicesArray = np.sort(indicesArray)
    return indicesArray
def ClusterDataBySpeedFastMovments(users):
    if users.__len__() < 2:
        return ('You need to choose at least 2 users to cluster')
    data = []
    for user in users:
        userarr = []
        # Choose How much round we want
        for i in range(4, 9):
            arr = [PointDrawing(user, i, 0, 1)]
            userarr.append(arr)
        data.append(userarr)
    ClusterValuesByPam(data, users)
def ClusterDataBySpeedVar(users):
    if users.__len__() < 2:
        return ('You need to choose at least 2 users to cluster')
    data = []
    for user in users:
        userarr = []
        # Choose How much round we want
        for i in range(4, 9):
            arr = [SpeedUpEyes(user, i, 1)]
            userarr.append(arr)
        data.append(userarr)
    ClusterValuesByPam(data, users)
def ClusterDataBySpeedAndFastMovmentAVG(users):
    if users.__len__() < 2:
        return ('You need to choose at least 2 users to cluster')
    data = []
    j = 0
    for user in users:
        print(user)
        userarr1 = []
        # Choose How much round we want
        for i in range(4, 9):
            arr = [SpeedUpEyes(user, i, 1)]
            userarr1.append(arr)
        tempArray = []
        tempArray.append((np.average(userarr1)))
        data.append(tempArray)
    for user in users:
        userarr2 = []
        # Choose How much round we want
        for i in range(4, 9):
            arr = [PointDrawing(user, i, 0, 1)]
            userarr2.append(arr)
        tempArray = 0
        tempArray = np.average(userarr2)
        data[j].append(tempArray)
        j += 1
    ClusterValuesByPamWithTwoFeatures(data, users)
def ClusterValuesByPam(data, users):
    k_medoids = KMedoids(n_cluster=2)
    k_medoids.fit(data)
    plot_graphs(data, k_medoids, users)
def plot_graphs(data, k_medoids, users):
    colors = {0: 'b*', 1: 'g^', 2: 'ro', 3: 'c*', 4: 'm^', 5: 'yo', 6: 'ko', 7: 'w*'}
    index = 0
    for key in k_medoids.clusters.keys():
        temp_data = k_medoids.clusters[key]
        x = [data[i][0] for i in temp_data]
        y = [data[i][1] for i in temp_data]
        plt.plot(x, y, colors[index])
        for i in range(temp_data.__len__()):
            xNumber = x[i]
            yNumber = y[i]
            plt.annotate(users[temp_data[i]], (xNumber[0], yNumber[0]), textcoords="offset points", xytext=(0, 5), ha='center')
        index += 1
    plt.title('Cluster By Speed Var')
    plt2PDFClusterByOneValue(plt)
    webbrowser.open_new(r'ClusterByOneValue.pdf')
    plt.show()
    medoid_data_points = []
    for m in k_medoids.medoids:
        medoid_data_points.append(data[m])
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    x_ = [i[0] for i in medoid_data_points]
    y_ = [i[1] for i in medoid_data_points]
    plt.plot(x, y, 'yo')
    plt.plot(x_, y_, 'r*')
    plt.title('Mediods are highlighted in red')
    plt.show()
def ClusterValuesByPamWithTwoFeatures(data, users):
    k_medoids = KMedoids(n_cluster=2)
    k_medoids.fit(data)
    plot_graphsWithTwoFeatures(data, k_medoids, users)
def plot_graphsWithTwoFeatures(data, k_medoids, users):
    colors = {0: 'b*', 1: 'g^', 2: 'ro', 3: 'c*', 4: 'm^', 5: 'yo', 6: 'ko', 7: 'w*'}
    index = 0
    for key in k_medoids.clusters.keys():
        temp_data = k_medoids.clusters[key]
        x = [data[i][0] for i in temp_data]
        y = [data[i][1] for i in temp_data]
        plt.plot(x, y, colors[index])
        for i in range(temp_data.__len__()):
            xNumber = x[i]
            yNumber = y[i]
            plt.annotate(users[temp_data[i]], (xNumber, yNumber), textcoords="offset points", xytext=(0, 5), ha='center')
        index += 1
    plt.title('Cluster by Transitions Movement and Speed Of eyes')
    plt.xlabel('Speed Variance Average')
    plt.ylabel('Transition Movement Average')
    #  plt.gca().axes.get_yaxis().set_visible(False)
   #  plt.gca().axes.get_xaxis().set_visible(False)
    plt2PDFClusterByTwoValues(plt)
    webbrowser.open_new(r'ClusterByTwoValues.pdf')
    plt.show()
    medoid_data_points = []
    for m in k_medoids.medoids:
        medoid_data_points.append(data[m])
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    x_ = [i[0] for i in medoid_data_points]
    y_ = [i[1] for i in medoid_data_points]
    plt.plot(x, y, 'yo')
    plt.plot(x_, y_, 'r*')
    plt.title('Mediods are highlighted in red')
    #  plt.show()

Main()