from PIL import Image

def blackOrWhite(pixel):
    if (2*pixel[0] - pixel[1] - pixel[2]) / 2 < 50:
        pix = (0,0,0)
    else:
        pix = (255,255,255)
    return pix 

def createTrainSet(index,item,angles):
    im = Image.open("raw/" + str(item) + "/img" + "%03d" % index + ".png")
    im = im.resize((im.width / 10, im.height / 10))
    #im = im.rotate(180) // rotate on nao becasue mine have rotated camera
    
    imagesFile = open("trainingData.txt", "a")
    for pixel in im.getdata():

        pix = blackOrWhite(pixel)
        #pix = pixel
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
        except Exception, e:
            #print e
            break

    return angles

if __name__ == "__main__":
    ar = ["bottom","bottom2","left","leftup","leftupup","right","rightup","rightup","top","top2"]
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
