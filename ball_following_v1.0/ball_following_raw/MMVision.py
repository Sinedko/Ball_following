'''
Created on 30. 7. 2012.

@author: Mika
'''

import naoqi

class VisionProxy(object):
    '''
    Class that wraps vision proxy
    '''

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