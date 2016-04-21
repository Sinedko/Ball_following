from PIL import Image

def blackOrWhite(pixel,fromm):
    if fromm == "NAO":
        plus = 0
    else: 
        plus = 20

    if (2*pixel[0] - pixel[1] - pixel[2]) / 2 < 50+plus: #50
        pix = (0,0,0)
    else:
        pix = (255,255,255)
    return pix 

def createTrainSet(index,item,angles):
    im = Image.open("raw/" + str(item) + "/img" + "%03d" % index + "-A.png")
    im1 = Image.open("raw/" + str(item) + "/img" + "%03d" % index + "-B.png")

    im = im.resize((im.width / 10, im.height / 10))
    im1 = im1.resize((im1.width / 10, im1.height / 10))
    #im = im.rotate(180) // rotate on nao becasue mine have rotated camera
   
    imagesFile = open("trainingData.txt", "a")
    for pixel in im.getdata():
        pix = blackOrWhite(pixel,"NAO")
        imagesFile.write(str(pix[0]) + " " + str(pix[1]) + " " + str(pix[2]) + " ")

    for pixel in im1.getdata():
        pix = blackOrWhite(pixel,"WEBCAM")
        imagesFile.write(str(pix[0]) + " " + str(pix[1]) + " " + str(pix[2]) + " ")

    actual1 = float(angles[index-1][0])
    actual2 = float(angles[index-1][1])
    
    end1 = float(angles[len(angles)-1][0])
    end2 = float(angles[len(angles)-1][1])

    if index != len(angles):
        imagesFile.write(str(end1 - actual1) + " " + str(end2 - actual2) + "\n")
    else:
        imagesFile.write(str(end1) + " " + str(end2) + "\n")
    

def relativeJoints(item):
    angles = []
    index = 1

    while True:
        try:
            jnts = open("raw/" + str(item) + "/angle" + "%03d" % index + ".dat")
            joints = jnts.readline().split()
            angles.append(joints)

            index += 1
        except:
            break

    return angles

if __name__ == "__main__":
    #ar = ["bottom","bottom2","left","left2","leftup","leftup2","leftupup","leftupup2","right","right2","rightup","rightup2","rightupup","rightupup2","top","topup","topup2","topupup"]
    #ar = ["bottom","left","left2","leftup","leftup2","leftupup","leftupup2","right","right2","rightup","rightup2","rightupup","rightupup2","top"]
    #ar = ["bottom","left","leftup","leftdown","top","right","rightup","rightdown"]
    ar = ["down","left","leftdown","leftup","right","rightdown","rightup","top"]
    #pyar = ["left","leftup","leftdown"]

    for item in ar:
        index = 1
        angles = relativeJoints(item)

        while True:
            try:
                createTrainSet(index,item,angles)
                index += 1
            except:
                print "Number of samples: %03d" % (index-1)
                break
