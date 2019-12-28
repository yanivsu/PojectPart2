import numpy as np
import math
from fpdf import FPDF
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
from pdf2image import convert_from_path, convert_from_bytes
import matplotlib.image as mpimg
from scipy.ndimage.filters import gaussian_filter
import mongoDB as db
def Main():
    print()
    # print(db.GetNumberOfRoundByUsername('mnb'))
    # print('Please enter your userName')
    # db.DominatValue('Yaniv', 21)
    # HeatMapFunction()
    # print(db.GetCoordinateByRoundNumber('Gulkin', 1))
    PointDrawing()
    # SpeedUpEyes()
    # CreateCardBoard(db.GetBoard('mnb', 232))
    # PDF2Image()
# MyPlot function helps to maps all the point into gaussian numbers
def myplot(x, y, s, bins=1000):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent
def PointDrawing():
    listOfCardByRound = db.GetBoard('Gulkin', 3)
    CreateCardBoard(listOfCardByRound)
    PDF2Image()
    listOfCoodinate = db.GetCoordinateByRoundNumber('Gulkin', 3)
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
def HeatMapFunction():
    #  Connect to DB and create a Board
    listOfCardByRound = db.GetBoard('Gulkin', 3)
    CreateCardBoard(listOfCardByRound)
    PDF2Image()
    listOfCoodinate = db.GetCoordinateByRoundNumber('Gulkin', 3)
    #  'Yaniv' Should replace to username
    xCor = []
    yCor = []
    #  Convert String point to float point
    for x in listOfCoodinate[0]:
        xCor.append(float(x))
    for y in listOfCoodinate[1]:
        yCor.append(float(y))
    plt.subplots(figsize=(12, 12))
    map_img = mpimg.imread('out.jpg')
    hmax = sns.kdeplot(xCor, yCor, cmap="Blues", shade=False)
    hmax.collections[0].set_alpha(0)
    plt.imshow(map_img, zorder=0, extent=[0, 2006, 0, 960], aspect='auto')
    #  Export File to PDF
    plt2PDF(plt)
    plt.show()
def SpeedUpEyes():
    f = open("305082950Middle20SEC.txt", "r")
    xCor = []
    yCor = []
    timeToGetPoints = 0
    pointsCount = 0
    deltaTimePerPoint = 0
    # Collect Points from textFile
    for line in f:
        tempLine = line.split()
        if (len(tempLine) > 2):
            timeToGetPoints = (float(tempLine[0]))
            deltaTimePerPoint = (float(tempLine[1]))
            pointsCount = (float(tempLine[2]))
        else:
            xCor.append(float(tempLine[0]))
            yCor.append(float(tempLine[1]))
    #Calcuate Distance
    distanceArray = []
    for i in range(len(xCor) - 1):
        firstPoint = [xCor[i], yCor[i]]
        secondPoint = [xCor[i+1], yCor[i+1]]
        tempDistacne = math.sqrt(math.pow((firstPoint[0] - secondPoint[0]), 2) + math.pow((firstPoint[1] - secondPoint[1]), 2))
        if (pointsCount <= 0) :
            break
    distanceArray.append(tempDistacne)
    # Data for plotting
    t = np.arange(0.0, timeToGetPoints, deltaTimePerPoint)
    fig, ax = plt.subplots()
    plt.plot(t, distanceArray, linestyle='solid')
    # ax.plot(t, s)
    # ax.set(xlabel='Time (s)', ylabel='Speed',
    #       title='About as simple as it gets, folks')
    # ax.grid()
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
def PDF2Image():
    # To user this function u must install Popper and put the path into System Path
    # You can use https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows
    images = convert_from_path('tempCardBoard.pdf', 500)
    for page in images:
        page.save('out.jpg', 'JPEG')
def plt2PDF(fig):
    fig.savefig("testPlot.pdf", bbox_inches='tight')
    return
Main()
