'''
Created on 16. 8. 2012.

@author: Mika
'''

import sys

def inputCode(x):
    """
    x = <0, 255>
    y = <-1, 1>
    Formula:
    y = ((2 * x) / 255) - 1
    """
    x = float(x)
    return ((2 * x) / 255) - 1

def inputDecode(x):
    """
    x = <0, 255>
    y = <-1, 1>
    Formula:
    x = ((255 * y) + 255) / 2
    """
    x = float(x)
    return ((255 * x) + 255) / 2

def outputCode(x):
    """
    x = <-4.1714, 4.1714>
    y = <0, 1>
    Formula:
    y = (x + 4.1714) / 8.3428
    """
    x = float(x)
    return (x + 4.1714) / 8.3428

def outputDecode(x):
    """
    x = <-4.1714, 4.1714>
    y = <0, 1>
    Formula:
    x = (y * 8.3428) - 4.1714
    """
    x = float(x)
    return (x * 8.3428) - 4.1714