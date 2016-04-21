import sys,time
from PIL import Image
import Classes

def storeImage(image,index):
    imageWidth = image[0]                                           # width of the image
    imageHeight = image[1]                                          # height of the image
    imageData = image[6]                                            # array of pixel values
    
    im = Image.frombytes("RGB", (imageWidth, imageHeight), imageData)
    im.save("raw/img" + str(index) + ".png")
    
def storeJointValues(joints, defaultJoints, index):
    with open("raw/angle" + str(index) + ".dat", "w") as jointsFile:
        #relativeJoints = []
        #for joint, default in zip(joints, defaultJoints):
        #    relativeJoints.append(joint[1] - default[1])
        #for joint in relativeJoints:
        for joint in joints:
            jointsFile.write(str(joint) + " ")

def main(ip, port):
    try:
        motionProxy = Classes.MotionProxy(ip, port)
        visionProxy = Classes.VisionProxy(ip, port)
        memoryProxy = Classes.MemoryProxy(ip, port)
        speakProxy = Classes.SpeakProxy(ip, port)
        postureProxy = Classes.PostureProxy(ip , port)
    except Exception, e:
        print "ERROR:"
        print e
        sys.exit(1)

    index = 0
    
    postureProxy.initPose(2)
    motionProxy.stiffnessOff("Head")
    
    defaultJoints = motionProxy.getJointValues("Head")
    
    speakProxy.saySomething("Train script succesfully started.")

    while not memoryProxy.getData("FrontTactilTouched"):
        pass

    speakProxy.saySomething("Recording.")
    
    while not memoryProxy.getData("RearTactilTouched"):
        defaultJoints = motionProxy.getJointValues("Head")
        
        image = visionProxy.getImage()
        joints = motionProxy.getJointValues("Head")

        index += 1
        
        try:
            storeImage(image,"%03d" % (index))
            storeJointValues(joints, defaultJoints,"%03d" % (index))
        except Exception, e:
            print "ERROR:"
            print e
            sys.exit(1)
    speakProxy.saySomething("End.")


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
        print "Usage: createTrain.py [IP] [PORT]"
        sys.exit(1)

    main(ip, port)