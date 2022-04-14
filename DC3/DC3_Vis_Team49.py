# File: DC3_Vis_Team49.py
# Date: 04/13/22
# By: 
# Jack Brunner
# jrbrunne
# Jackson Ferry-Zamora
# jferryza
# Vera Fong
# lfong22
# Hannah Kadlec
# hkadlec
# Section: 3
# Team: 49
#
# ELECTRONIC SIGNATURE
# Jack Brunner
# Jackson Ferry-Zamora
# Vera Fong
# Hannah Kadlec
#
# The electronic signatures above indicate that the program
# submitted for evaluation is the combined effort of all
# team members and that each member of the team was an
# equal participant in its creation. In addition, each
# member of the team has a general understanding of
# all aspects of the program development and execution.
#
# PROVIDE A BRIEF DESCRIPTION OF WHAT THE PROGRAM OR FUNCTION DOES 
# This code takes data from the specified file to make a greyscale image from the scan data

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image as im

def makeImage(fileName, size): # returns a greyscale and bw image
    # fileName = "C:\\Users\\hkadl\\Documents\\Purdue Spring 22\\ENGR162\\GitHub_Project3\\DC3\\DC3_Scan_Team49_image1.csv"
    # size = 25
    BWcutoff = 200

    fid = open(fileName, "r")
    data = fid.readlines()
    fid.close()

    # print(data)

    numPoints = len(data)
    numRows = size
    numCols = int(numPoints / size)
    print("imsize: ", numCols, numRows)

    arrayGS = np.zeros([size, size], dtype=np.int16)
    arrayBW = np.zeros([size, size], dtype=np.int16)
    for d in data:
        dataPoint = d.split(",") # Split each data point into [x, y, value]
        # print("{}, {}".format(dataPoint[2], int(dataPoint[2])))
        arrayGS[int(dataPoint[0]), int(dataPoint[1])] = int(dataPoint[2])
        arrayBW[int(dataPoint[0]), int(dataPoint[1])] = int(int(dataPoint[2]) > BWcutoff) * 255


    # print(arrayBW)
    img = im.fromarray(arrayGS)
    plt.imshow(img)
    plt.show()

    imgBW = im.fromarray(arrayBW)
    plt.imshow(imgBW)
    plt.show()
    # img.save("img1test.png")
    print("image done")


makeImage("DC3_Data.csv", 25)
print("done")