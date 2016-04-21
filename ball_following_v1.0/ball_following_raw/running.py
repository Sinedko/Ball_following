'''
Created on 8. 8. 2012.

@author: Mika
'''

import sys
import Image
import subprocess
import coding
import MMMotion
import MMVision
import MMMemory

def saveRGBValues(image):
    imageWidth = image[0]                                           # width of the image
    imageHeight = image[1]                                          # height of the image
    imageData = image[6]                                            # array of pixel values
    
    im = Image.fromstring("RGB", (imageWidth, imageHeight), imageData)
    im = im.resize((imageWidth / 10, imageHeight / 10))
    
    with open("image.txt", "w") as imageFile:
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
        
        nn_run = subprocess.Popen("NNRun.exe", shell=True, stdout=subprocess.PIPE)
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
            
            if joints[0] < -2.0857 or joints[0] > 2.0857:
                continue
            if joints[1] < -0.6720 or joints[1] > 0.5149:
                continue
            
            motionProxy.setJointValues("Head", joints)

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