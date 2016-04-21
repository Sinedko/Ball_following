'''
Created on 30. 7. 2012.

@author: Mika
'''

import naoqi
import motion

class MotionProxy(object):
    '''
    Class that wraps motion proxy
    '''
    
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
        HeadYawAngle       = + 0.0
        HeadPitchAngle     = + 0.0
    
        ShoulderPitchAngle = +80.0
        ShoulderRollAngle  = +20.0
        ElbowYawAngle      = -80.0
        ElbowRollAngle     = -60.0
        WristYawAngle      = + 0.0
        HandAngle          = + 0.0
    
        HipYawPitchAngle   = + 0.0
        HipRollAngle       = + 0.0
        HipPitchAngle      = -25.0
        KneePitchAngle     = +40.0
        AnklePitchAngle    = -20.0
        AnkleRollAngle     = + 0.0
        
        Head     = [HeadYawAngle, HeadPitchAngle]

        LeftArm  = [ShoulderPitchAngle, +ShoulderRollAngle, +ElbowYawAngle, +ElbowRollAngle, WristYawAngle, HandAngle]
        RightArm = [ShoulderPitchAngle, -ShoulderRollAngle, -ElbowYawAngle, -ElbowRollAngle, WristYawAngle, HandAngle]

        LeftLeg  = [HipYawPitchAngle, +HipRollAngle, HipPitchAngle, KneePitchAngle, AnklePitchAngle, +AnkleRollAngle]
        RightLeg = [HipYawPitchAngle, -HipRollAngle, HipPitchAngle, KneePitchAngle, AnklePitchAngle, -AnkleRollAngle]
        
        pTargetAngles = Head + LeftArm + LeftLeg + RightLeg + RightArm
        pTargetAngles = [x * motion.TO_RAD for x in pTargetAngles]

        pNames = "Body"
        pMaxSpeedFraction = 0.2
        
        self.__proxy.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)
    
    def getJointValues(self, names):
        useSensors = True   # take values from sensors and not commands
        
        jointNames = self.__proxy.getJointNames(names)
        jointValues = self.__proxy.getAngles(names, useSensors)

        joints = zip(jointNames, jointValues)
        return joints   # list of joint pairs [(name, value)]
    
    def setJointValues(self, names, values):
        speed = 0.05
        self.__proxy.angleInterpolationWithSpeed(names, values, speed)