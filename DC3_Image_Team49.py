import numpy as np
from matplotlib import pyplot as plt
from PIL import Image as im

# A = [0, 255, 0, 255]
# x = [1, 2, 3, 4, 5]
# y = [1, 2, 6, 1, 5]
def makeImage():
    fileName = "C:\\Users\\hkadl\\Documents\\Purdue Spring 22\\ENGR162\\GitHub_Project3\\DC3\\DC3_Scan_Team49_image1.csv"
    size = 25
    BWcutoff = 200


    fid = open(fileName, "r")
    data = fid.readlines()
    fid.close()

    print(data)

    numPoints = len(data)
    numRows = size
    numCols = int(numPoints / size)
    print("imsize: ", numCols, numRows)

    arrayGS = np.zeros([size, size], dtype=np.int16)
    arrayBW = np.zeros([size, size], dtype=np.int16)
    for d in data:
        dataPoint = d.split(",") # Split each data point into [x, y, value]
        print("{}, {}".format(dataPoint[2], int(dataPoint[2])))
        arrayGS[int(dataPoint[0]), int(dataPoint[1])] = int(dataPoint[2])
        arrayBW[int(dataPoint[0]), int(dataPoint[1])] = int(int(dataPoint[2]) > BWcutoff) * 255


    print(arrayBW)
    img = im.fromarray(arrayGS)
    plt.imshow(img)
    plt.show()

    imgBW = im.fromarray(arrayBW)
    plt.imshow(imgBW)
    plt.show()
    # img.save("img1test.png")
    print("image done")


# plt.imshow(np.array(A))
# plt.plot(x,y)
# plt.show()
print("done")