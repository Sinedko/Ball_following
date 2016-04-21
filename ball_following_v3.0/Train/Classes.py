import naoqi
import motion

class SpeakProxy(object):

    def __init__(self, ip, port):
        self.__proxy = naoqi.ALProxy("ALTextToSpeech", ip, port)

    def saySomething(self, message):
        self.__proxy.say(str(message))

class PostureProxy(object):

    def __init__(self, ip, port):
        self.__proxy = naoqi.ALProxy("ALRobotPosture", ip, port)

    def initPose(self, number):
        pose = ""
        if int(number) == 1:
            pose = "Stand"
        elif int(number) == 2:
            pose = "StandInit"
        elif int(number) == 3:
            pose = "StandZero"
        elif int(number) == 4:
            pose = "Crouch"
        elif int(number) == 5:
            pose = "Sit"
        elif int(number) == 6:
            pose = "SitRelax"
        else:
            pose = "StandInit"

        self.__proxy.goToPosture(pose, 1.0)

class MemoryProxy(object):

    def __init__(self, ip, port):
        self.__proxy = naoqi.ALProxy("ALMemory", ip, port)
    
    def getData(self, names):
        data = self.__proxy.getData(names)
        return data     # value of names from ALMemory

class MotionProxy(object):

    def __init__(self, ip, port):
        self.__proxy = naoqi.ALProxy("ALMotion", ip, port)
        

    def stiffnessOn(self, names):
        stiffnessLists = 1.0    # maximum stiffness, turn motors on
        timeLists = 1.0         # one second
        
        self.__proxy.stiffnessInterpolation(names, stiffnessLists, timeLists)
    
    def stiffnessOff(self, names):
        stiffnessLists = 0.0    # minimum stiffness, turn motors off
        timeLists = 1.0         # one second
        
        self.__proxy.stiffnessInterpolation(names, stiffnessLists, timeLists)
    
    def poseInit(self):
        self._posture.goToPosture("StandInit", 1.0)
    
    def getJointValues(self, names):
        useSensors = True   # take values from sensors and not commands
        
        jointNames = self.__proxy.getJointNames(names)
        jointValues = self.__proxy.getAngles(names, useSensors)

        joints = zip(jointNames, jointValues)
        return joints   # list of joint pairs [(name, value)]
    
    def setJointValues(self, names, values):
        speed = 0.05
        self.__proxy.angleInterpolationWithSpeed(names, values, speed)

class VisionProxy(object):

    def __init__(self, ip, port):
        self.__proxy = naoqi.ALProxy("ALVideoDevice", ip, port)
    
    def getImage(self):
        resolution = 1      # QVGA 320x240
        colorSpace = 11     # RGB
        fps = 30            # 30 frames/second
        
        videoModule = self.__proxy.subscribe("videoModule", resolution, colorSpace, fps)
        image = self.__proxy.getImageRemote(videoModule)
        
        self.__proxy.releaseImage(videoModule)
        self.__proxy.unsubscribe(videoModule)
        
        return image    #list of data about image (References->API->Vision->ALVideoDevice)

def inputCode(x):
    x = float(x)
    return ((2 * x) / 255) - 1
    """
    x = <0, 255>
    y = <-1, 1>
    Formula:
    y = ((2 * x) / 255) - 1
    """

def inputDecode(x):
    x = float(x)
    return ((255 * x) + 255) / 2
    """
    x = <0, 255>
    y = <-1, 1>
    Formula:
    x = ((255 * y) + 255) / 2
    """

def outputCode(x):
    x = float(x)
    return (x + 4.1714) / 8.3428
    """
    x = <-4.1714, 4.1714>
    y = <0, 1>
    Formula:
    y = (x + 4.1714) / 8.3428
    """

def outputDecode(x):
    x = float(x)
    return (x * 8.3428) - 4.1714
    """
    x = <-4.1714, 4.1714>
    y = <0, 1>
    Formula:
    x = (y * 8.3428) - 4.1714
    """