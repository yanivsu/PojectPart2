import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter


def Main():
     HeatMapFunction()
     PointDrawing()
     SpeedUpEyes()

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
    xCor.append(float(2006))
    yCor.append(float(890))
    ax = plt.axes()
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
    axs.imshow(img, extent=extent, cmap=cm.jet) # Extent => ratio 16:9 cmap.jet => Looks like really heat map
    axs.set_title("Heat Map")
    plt.show()
    return
def SpeedUpEyes():
    f = open("305082950Middle20SEC.txt", "r")
    xCor = []
    yCor = []
    # Collect Points from textFile
    for line in f:
        tempLine = line.split()
        xCor.append(float(tempLine[0]))
        yCor.append(float(tempLine[1]))
    #Calcuate Distance
    distanceArray = []
    for i in range(len(xCor) - 1):
        firstPoint = [xCor[i], yCor[i]]
        secondPoint = [xCor[i+1], yCor[i+1]]
        tempDistacne = math.sqrt(math.pow((firstPoint[0] - secondPoint[0]), 2) + math.pow((firstPoint[1] - secondPoint[1]), 2));
        distanceArray.append(tempDistacne)
    # Data for plotting
    t = np.arange(0.0, 20.0, 0.02)
    distanceArray = distanceArray[0:1000]
    print(len(t))
    print(len(distanceArray))
    fig, ax = plt.subplots()
    plt.plot(t, distanceArray, linestyle='solid')
    # ax.plot(t, s)
    # ax.set(xlabel='Time (s)', ylabel='Speed',
    #       title='About as simple as it gets, folks')
    # ax.grid()
    plt.show()


Main()
