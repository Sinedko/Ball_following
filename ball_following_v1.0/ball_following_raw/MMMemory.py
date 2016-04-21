'''
Created on 30. 7. 2012.

@author: Mika
'''

import naoqi

class MemoryProxy(object):
    '''
    Class that wraps memory proxy
    '''

    def __init__(self, ip, port):
        self.__proxy = naoqi.ALProxy("ALMemory", ip, port)
    
    def getData(self, names):
        data = self.__proxy.getData(names)
        return data     # value of names from ALMemory