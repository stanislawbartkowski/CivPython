'''
Created on 1 lut 2019

@author: civ
'''

from enum import Enum
from com.civ.play.misc import MapCR

class Command(Enum):
    SETCAPITAL = 1
    SETSCOUT = 2
    SETARMY = 3
    BUYARTILLERY = 4
    BUYINFANTRY = 5
    BUYMOUNTED = 6
    BUYAIRCRAFT = 7
    BUYARMY = 8
    BUYSCOUT = 9
    STARTMOVE = 10
    MOVE = 11
    REVEALTILE = 12
    ENDOFMOVE = 13
    ENDOFPHASE = 14
    RESEARCH = 15
    EXPLOREHUT = 16
    HARVESTRESOURCE = 17
    SENDPRODUCTION = 18
    BUYBUILDING = 19
    DEVOUTTOCULTURE = 20
    ADVANCECULTURE = 21
    SPENDTRADE = 22
    DISCARDCARD = 23
    BUYWONDER = 24
        
_map = {
  "SETCAPITAL" : Command.SETCAPITAL,
  "SETSCOUT" : Command.SETSCOUT,
  "SETARMY" : Command.SETARMY,
  "BUYARTILLERY" : Command.BUYARTILLERY,
  "BUYINFANTRY" : Command.BUYINFANTRY,
  "BUYMOUNTED" : Command.BUYMOUNTED,
  "BUYAIRCRAFT" : Command.BUYAIRCRAFT,
  "BUYARMY" : Command.BUYARMY,
  "BUYSCOUT" : Command.BUYSCOUT,
  "STARTMOVE" : Command.STARTMOVE,
  "MOVE" : Command.MOVE,
  "REVEALTILE" : Command.REVEALTILE,
  "ENDOFMOVE" : Command.ENDOFMOVE,
  "ENDOFPHASE" : Command.ENDOFPHASE,
  "RESEARCH" : Command.RESEARCH,
  "EXPLOREHUT" : Command.EXPLOREHUT,
  "HARVESTRESOURCE" : Command.HARVESTRESOURCE,
  "SENDPRODUCTION" : Command.SENDPRODUCTION,
  "BUYBUILDING" : Command.BUYBUILDING,
  "DEVOUTTOCULTURE" : Command.DEVOUTTOCULTURE,
  "ADVANCECULTURE" : Command.ADVANCECULTURE,
  "SPENDTRADE" : Command.SPENDTRADE,
  "DISCARDCARD" : Command.DISCARDCARD,
  "BUYWONDER" : Command.BUYWONDER
}

_M = MapCR(_map) 

def toCommand(s): return _M.toC(s)

def isCommand(s): return _M.isC(s)

def toS(v) : return _M.toK(v)

def isMove(c):
    return c == Command.Move or c == Command.REVEALTILE or c == Command.ENDOFMOVE or c == Command.EXPLOREHUT
