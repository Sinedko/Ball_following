'''
Created on 30. 7. 2012.

@author: Mika
'''

import sys
import time
import Image
import coding
import MMMotion
import MMVision
import MMMemory

def storeImage(image):
    imageWidth = image[0]                                           # width of the image
    imageHeight = image[1]                                          # height of the image
    imageData = image[6]                                            # array of pixel values
    imageTimestamp = float(image[4]) + ((image[5] / 10000) * 0.01)  # timestamp of the image
    
    im = Image.fromstring("RGB", (imageWidth, imageHeight), imageData)
    im = im.resize((imageWidth / 10, imageHeight / 10))
    
    px = im.load()
    
    with open("images.txt", "a") as imagesFile:
        width, height = im.size
        for x in range(width):
            for y in range(height):
                if (2*px[x,y][0] - px[x,y][1] - px[x,y][2]) / 2 < 50:
                    px[x,y] = (0,0,0)
                else:
                    px[x,y] = (255,255,255)
        
        for pixel in im.getdata():
            p1 = coding.inputCode(pixel[0])
            p2 = coding.inputCode(pixel[1])
            p3 = coding.inputCode(pixel[2])
            imagesFile.write(str(p1) + " " + str(p2) + " " + str(p3) + " ")
        imagesFile.write("\n")

def storeJointValues(joints, defaultJoints):
    with open("joints.txt", "a") as jointsFile:
        relativeJoints = []
        for joint, default in zip(joints, defaultJoints):
            relativeJoints.append(joint[1] - default[1])
        for joint in relativeJoints:
            j = coding.outputCode(joint)
            jointsFile.write(str(j) + " ")
        jointsFile.write("\n")

def main(ip, port):
    try:
        motionProxy = MMMotion.MotionProxy(ip, port)
        visionProxy = MMVision.VisionProxy(ip, port)
        memoryProxy = MMMemory.MemoryProxy(ip, port)
    except Exception, e:
        print "ERROR:"
        print e
        sys.exit(1)
    
    motionProxy.stiffnessOn("Body")
    motionProxy.poseInit()
    motionProxy.stiffnessOff("Head")
    
    defaultJoints = motionProxy.getJointValues("Head")
    
    while not memoryProxy.getData("LeftBumperPressed"):
        pass
    
    while not memoryProxy.getData("RightBumperPressed"):
        motionProxy.stiffnessOn("Body")
        motionProxy.poseInit()
        motionProxy.stiffnessOff("Head")
        
        image = visionProxy.getImage()
        joints = motionProxy.getJointValues("Head")
        
        try:
            storeImage(image)
            storeJointValues(joints, defaultJoints)
        except Exception, e:
            print "ERROR:"
            print e
            sys.exit(1)

if __name__ == "__main__":
    ip = "127.0.0.1"        #default IP address
    port = 9559             #default port

    if len(sys.argv) == 2:
        ip = sys.argv[1]
    elif len(sys.argv) == 3:
        ip = sys.argv[1]
        port = sys.argv[2]
    elif len(sys.argv) > 3:
        print "ERROR:"
        print "Wrong number of parameters."
        print "Usage: collecting.py [IP] [PORT]"
        sys.exit(1)

    main(ip, port)