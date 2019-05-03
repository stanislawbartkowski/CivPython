'''
Created on 1 maj 2019

@author: civ
'''

from enum import Enum
from com.civ.play.misc import MapCR


class Resource(Enum):
    CULTURE = 1
    
_map = { 'Culture' : Resource.CULTURE }

_M = MapCR(_map) 

def toR(r) : return _M.toC(r)

def toS(r) : return _M.toK(r)
