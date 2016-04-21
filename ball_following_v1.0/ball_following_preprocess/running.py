'''
Created on 8. 8. 2012.

@author: Mika
'''

import sys
from PIL import Image
import subprocess
import coding
import MMMotion
import MMVision
import MMMemory
from naoqi import ALProxy

def saveRGBValues(image):
    imageWidth = image[0]                                           # width of the image
    imageHeight = image[1]                                          # height of the image
    imageData = image[6]                                            # array of pixel values
    
    im = Image.frombytes("RGB", (imageWidth, imageHeight), imageData)
    im = im.resize((imageWidth / 10, imageHeight / 10))
    im = im.rotate(180)

    px = im.load()
    
    with open("image.txt", "w") as imageFile:
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
            imageFile.write(str(p1) + "\n" + str(p2) + "\n" + str(p3) + "\n")

def main(ip, port):
    try:
        motionProxy = MMMotion.MotionProxy(ip, port)
        visionProxy = MMVision.VisionProxy(ip, port)
        memoryProxy = MMMemory.MemoryProxy(ip, port)
        sayproxy = ALProxy("ALTextToSpeech", "192.168.1.100", 9559)
        sayproxy.say("Started")
    except Exception, e:
        print "ERROR:"
        print e
        sys.exit(1)
    
    motionProxy.stiffnessOn("Body")
    motionProxy.poseInit()
    
    while not memoryProxy.getData("FrontTactilTouched"):
        pass
    
    while not memoryProxy.getData("RearTactilTouched"):
        image = visionProxy.getImage()
        naoJoints = motionProxy.getJointValues("Head")
        saveRGBValues(image)
        
        nn_run = subprocess.Popen("./NNRun.bin", shell=True, stdout=subprocess.PIPE)
        nn_run.wait()
        if nn_run.returncode == 0:
            relativeJoints = nn_run.stdout.read()
            relativeJoints = relativeJoints.split()
            relativeJoints = [float(x) for x in relativeJoints]
            relativeJoints = [coding.outputDecode(x) for x in relativeJoints]

            join1 = open("join1.txt", "a")
            join2 = open("join2.txt", "a")
            join1.write(str(relativeJoints[0])+" ")
            join2.write(str(relativeJoints[1])+" ")
            
            joints = []
            for joint, nao in zip(relativeJoints, naoJoints):
                joints.append(joint + nao[1])
            
            if joints[0] < -2.0857 or joints[0] > 2.0857: # dolava dprava max
                continue
            if joints[1] < -0.6720 or joints[1] > 0.5149: #hore dole max
                continue
            
            motionProxy.setJointValues("Head", joints)
   
    motionProxy.stiffnessOn("Body")
    motionProxy.poseInit()


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
        print "Usage: running.py [IP] [PORT]"
        sys.exit(1)

    main(ip, port)