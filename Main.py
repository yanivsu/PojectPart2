import numpy as np
import math
from fpdf import FPDF
from PIL import Image
from os import listdir
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter


def Main():
    # HeatMapFunction()
    # PointDrawing()
    # SpeedUpEyes()
     CreateCardBoard()

# MyPlot function helps to maps all the point into gaussian numbers
def myplot(x, y, s, bins=1000):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent
def PointDrawing():
    f = open("305082950Middle20SEC.txt", "r")
    xCor = []
    yCor = []
    # Collect Points from textFile
    for line in f:
        tempLine = line.split()
        xCor.append(float(tempLine[0]))
        yCor.append(float(tempLine[1]))
    #  xCor.append(float(2006))
    #  yCor.append(float(890))
    ax = plt.axes()
    ax.set(xlim=(0, 2500), ylim=(0, 960))
    ax.plot(xCor, yCor, 'bo-')
    plt.show()
    return
def HeatMapFunction():
    f = open("305082950Middle20SEC.txt", "r")
    xCor = []
    yCor = []
    # Collect Points from textFile
    for line in f:
        tempLine = line.split()
        xCor.append(float(tempLine[0]))
        yCor.append(float(tempLine[1]))
    # Add x Point and y Point
    xCor.append(float(2006))
    yCor.append(float(890))

    fig, axs = plt.subplots(1, 1)
    img, extent = myplot(xCor, yCor, 64)
    axs.imshow(img, extent=extent, cmap=cm.jet)  # Extent => ratio 16:9 cmap.jet => Looks like really heat map
    axs.set_title("Heat Map")
    plt.show()
    return
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
def CreateCardBoard():
    path = '/Users/yanivsuriyano/PycharmProjects/PojectPart2/allcards/'  # get the path of images
    imagelist = listdir(path)  # get list of all images
    pdf = FPDF('P', 'mm', 'A4')  # create an A4-size pdf document
    pdf.add_page()
    x, y, w, h = 0, 42.6, 43.6, 27.7
    i = 0
    for image in imagelist:
        if (x == 131.39999999999998):
            x = 43.8
            y = y + 27.9
        else:
            x = x + 43.8
        print(i)
        print(x)
        pdf.image(path + image, x, y, w, h)
        # The if condition should be removed soon
        if(i < 12):
            i = i + 1
        if(i == 12):
            break
    pdf.output("images.pdf", "F")
Main()
