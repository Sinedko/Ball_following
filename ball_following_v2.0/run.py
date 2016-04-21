import sys,subprocess
#import cv2.cv as cv
import Classes
from PIL import Image

def saveRGBValues(image,fromDevice):
    im = 0
    imageWidth = 320
    imageHeight = 240
    
    if fromDevice == 'NAO':
        imageWidth = image[0]                                           # width of the image
        imageHeight = image[1]                                          # height of the image
        imageData = image[6]                                            # array of pixel values
    
        im = Image.frombytes("RGB", (imageWidth, imageHeight), imageData)
        #im = im.rotate(180) --> use this when you have normal nao with normal cam ! :P
    elif fromDevice == 'WEBCAM':
        #im = Image.fromstring("RGB", cv.GetSize(image), image.tostring())
        im = image
    #im.show()
    im = im.resize((imageWidth / 10, imageHeight / 10))

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
            p1 = Classes.inputCode(pixel[0])
            p2 = Classes.inputCode(pixel[1])
            p3 = Classes.inputCode(pixel[2])
            imageFile.write(str(p1) + "\n" + str(p2) + "\n" + str(p3) + "\n")

def getImageFromCam():
    capture = cv.CaptureFromCAM(0)

    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    img = cv.QueryFrame(capture)
    cv.SaveImage('img.png',img)

    img = Image.open('img.png')

    return img

def main(ip, port):
    try:
        motionProxy  = Classes.MotionProxy(ip, port)
        visionProxy  = Classes.VisionProxy(ip, port)
        memoryProxy  = Classes.MemoryProxy(ip, port)
        speakProxy   = Classes.SpeakProxy(ip, port)
        postureProxy = Classes.PostureProxy(ip, port) 
    except Exception, e:
        print "ERROR:"
        print e
        sys.exit(1)
    speakProxy.saySomething('Script succesfully started.')
    
    #motionProxy.stiffnessOn("Body")
    postureProxy.initPose(2)
    
    while not memoryProxy.getData("FrontTactilTouched"):
        pass
    
    while not memoryProxy.getData("RearTactilTouched"):
        image = visionProxy.getImage()
        #image = getImageFromCam()
        naoJoints = motionProxy.getJointValues("Head")
        saveRGBValues(image,'NAO')
        #saveRGBValues(image,'WEBCAM')
        
        nn_run = subprocess.Popen("./backprop", shell=True, stdout=subprocess.PIPE)
        nn_run.wait()
        if nn_run.returncode == 0:
            relativeJoints = nn_run.stdout.read()
            relativeJoints = relativeJoints.split()
            relativeJoints = [float(x) for x in relativeJoints]
            relativeJoints = [Classes.outputDecode(x) for x in relativeJoints]

            """
            join1 = open("join1.txt", "a")
            join2 = open("join2.txt", "a")
            join1.write(str(relativeJoints[0])+" ")
            join2.write(str(relativeJoints[1])+" ")
            """
            
            joints = []
            for joint, nao in zip(relativeJoints, naoJoints):
                joints.append(joint + nao[1])

            if joints[0] < -2.0857 or joints[0] > 2.0857: # dolava dprava max
                continue
            if joints[1] < -0.6720 or joints[1] > 0.5149: #hore dole max
                continue
            
            motionProxy.setJointValues("Head", joints)
   
    postureProxy.initPose(4)
    speakProxy.saySomething("Bye Bye")
    motionProxy.stiffnessOff("Body")
    motionProxy.stiffnessOff("Head")

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
        print "Usage: run.py [IP] [PORT]"
        sys.exit(1)

    main(ip, port)

