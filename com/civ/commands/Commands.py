'''
Created on 1 lut 2019

@author: civ
'''

from enum import Enum


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
    

SETCAPITAL = "SETCAPITAL"
SETSCOUT = "SETSCOUT"
SETARMY = "SETARMY"
BUYARTILLERY = "BUYARTILLERY"
BUYINFANTRY = "BUYINFANTRY"
BUYMOUNTED = "BUYMOUNTED"
BUYAIRCRAFT = "BUYAIRCRAFT"
BUYARMY = "BUYARMY"
BUYSCOUT = "BUYSCOUT"
STARTMOVE = "STARTMOVE"
MOVE = "MOVE"
REVEALTILE = "REVEALTILE"
ENDOFMOVE = "ENDOFMOVE"
ENDOFPHASE = "ENDOFPHASE"
RESEARCH = "RESEARCH"
EXPLOREHUT = "EXPLOREHUT"
HARVESTRESOURCE = "HARVESTRESOURCE"


def toCommand(s):
    if s == SETCAPITAL : return Command.SETCAPITAL
    if s == SETSCOUT : return Command.SETSCOUT
    if s == SETARMY : return Command.SETARMY
    if s == BUYARTILLERY : return Command.BUYARTILLERY
    if s == BUYINFANTRY : return Command.BUYINFANTRY
    if s == BUYMOUNTED : return Command.BUYMOUNTED
    if s == BUYAIRCRAFT : return Command.BUYAIRCRAFT
    if s == BUYARMY : return Command.BUYARMY
    if s == BUYSCOUT : return Command.BUYSCOUT
    if s == STARTMOVE : return Command.STARTMOVE
    if s == MOVE : return Command.MOVE
    if s == REVEALTILE : return Command.REVEALTILE
    if s == ENDOFMOVE : return Command.ENDOFMOVE
    if s == ENDOFPHASE : return Command.ENDOFPHASE
    if s == RESEARCH : return Command.RESEARCH
    if s == EXPLOREHUT : return Command.EXPLOREHUT
    if s == HARVESTRESOURCE : return Command.HARVESTRESOURCE
    return None


def toS(c):
    if c == Command.SETCAPITAL : return SETCAPITAL
    if c == Command.SETSCOUT : return SETSCOUT
    if c == Command.SETARMY : return SETARMY
    if c == Command.BUYARTILLERY : return BUYARTILLERY
    if c == Command.BUYINFANTRY : return BUYINFANTRY
    if c == Command.BUYMOUNTED : return BUYMOUNTED
    if c == Command.BUYAIRCRAFT : return BUYAIRCRAFT
    if c == Command.BUYARMY : return BUYARMY
    if c == Command.BUYSCOUT : return BUYSCOUT
    if c == Command.STARTMOVE : return STARTMOVE
    if c == Command.MOVE : return MOVE
    if c == Command.REVEALTILE : return REVEALTILE
    if c == Command.ENDOFMOVE : return ENDOFMOVE
    if c == Command.ENDOFPHASE : return ENDOFPHASE
    if c == Command.RESEARCH : return RESEARCH
    if c == Command.EXPLOREHUT : return EXPLOREHUT
    if c == Command.HARVESTRESOURCE : return HARVESTRESOURCE
    return None


def isMove(c):
    return c == Command.Move or c == Command.REVEALTILE or c == Command.ENDOFMOVE or c == Command.EXPLOREHUT
