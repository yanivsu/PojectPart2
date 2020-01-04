import numpy as np
import math
from fpdf import FPDF
import cv2
import seaborn as sns
import matplotlib.pyplot as plt
from pdf2image import convert_from_path, convert_from_bytes
import matplotlib.image as mpimg
from scipy.ndimage.filters import gaussian_filter
import mongoDB as db
def Main():
    # print(db.GetNumberOfRoundByUsername('mnb'))
    # print('Please enter your userName')
    # db.DominatValue('Yaniv', 21)
    # HeatMapFunction()
    # print(db.GetCoordinateByRoundNumber('Gulkin', 1))
    # PointDrawing()
    # SpeedUpEyes()
    # CreateCardBoard(db.GetBoard('mnb', 232))
    # PDF2Image()
    CreateDominantCardBoard()
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
    listOfCoodinate = db.GetCoordinateByRoundNumber('Gulkin', 1)
    #  'Yaniv' Should replace to username
    xCor = []
    yCor = []
    #  Convert String point to float point
    for x in listOfCoodinate[0]:
        xCor.append(float(x))
    for y in listOfCoodinate[1]:
        yCor.append(float(y))
    timeOfRound = db.GetTimeDeatilsPerRound('Gulkin', 1)[1]
    pointsCount = xCor.__len__()
    deltaTimePerPoint = pointsCount / timeOfRound
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
def CreateDominantCardBoard():
    listOfCardByRound = db.DominatValue('Gulkin', 3)
    if listOfCardByRound == False:
        print('Sorry the round has no dominant value')
        return False
    print('The dominant board creation is in process...')
    path = 'allcards/'  # get the path of images
    tempPath = 'tenocardboard/'
    imageListHighlight = []
    imageList = []
    #  Get the card list of dominant value from board
    for i in range(listOfCardByRound.__len__()):
        imageListHighlight.append(listOfCardByRound[i]+'.png')
    #  Get the all board
    listOfCardByRound = db.GetBoard('Gulkin', 3)
    for i in range(12):
        imageList.append(listOfCardByRound[str(i)] + '.png')
    #Create New Board with highlight cards
    for i in range(12):
        for j in range(imageListHighlight.__len__()):
            if imageList[i] == imageListHighlight[j]:
             img = cv2.imread(tempPath + imageListHighlight[1])
             blur_image = cv2.GaussianBlur(img, (51, 51), 0)
             cv2.imwrite(path + imageList[i], blur_image)
    #  The GaussianBlur() uses the Gaussian kernel.
    #  The height and width of the kernel should be a positive and an odd number.
    #  Then you have to specify the X and Y direction that is sigmaX and sigmaY respectively.
    #  If only one is specified, both are considered the same.
    pdf = FPDF('L', 'mm', 'A4')  # create an A4-size pdf document
    pdf.add_page()
    pdf.output("tempCardHighlightBoard.pdf", "F")
    print('The dominant board creation is in finished ...')

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
