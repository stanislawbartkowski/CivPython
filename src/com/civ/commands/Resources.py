'''
Created on 1 maj 2019

@author: civ
'''

from enum import Enum
from com.civ.play.misc import MapCR


class Resource(Enum):
    CULTURE = 1
    INCENSE = 2
    SILK = 3
    
class HV(Enum):
    HUT=1
    VILLAGE=2    
    
_map = { 'Culture' : Resource.CULTURE,"Incense" : Resource.INCENSE, "Silk" : Resource.SILK }
_map1 = { "Hut" : HV.HUT, "Village" : HV.VILLAGE } 

_M = MapCR(_map) 
_M1 = MapCR(_map1) 

def toR(r) : return _M.toC(r)
def toS(r) : return _M.toK(r)

def toHV(r): return _M1.toC(r)
def toHVS(r): return _M1.toK(r)


