'''
Created on 15 lut 2019

@author: civ
'''

import os

if __name__ == '__main__':
    d = os.curdir
    print(d)
    c = os.path.dirname(os.path.abspath(__file__))
    print(c)
