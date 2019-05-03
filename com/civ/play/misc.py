'''
Created on 1 lut 2019

@author: civ
'''

from com.civ.rest import CivRest as C
import random
import json

def joinGame():
    gameid = C.getGameid()
    games = C.getWaitingGames()
    civwaiting = C.findGame(games, gameid)
    token = C.joinGame(gameid, civwaiting).split(',')[0]
    return (token, gameid)


def getRandom(a, selfun=None):
    if len(a) == 0 : return None
    if selfun == None :
        i = random.randrange(0, len(a))
        return a[i]
    for elem in a :
        if selfun(elem) : return elem
    return None    


def pToJ(row, col):
    m = {"row" : row, "col" : col}
    return json.dumps(m)


def eqP(p1, p2):
    return (p1["row"] == p2["row"]) and (p1["col"] == p2["col"])


class MapCR : 
    
    def __init__(self,map):
        self._map = map
        
    def toC(self,k):
        return self._map[k]
    
    def isC(self,k): 
        return self._map.get(k) != None

    def toK(self,val):
        for e in self._map.items() : 
            if e[1] == val : return e[0]
        raise Exception('Value does not exist in the map', val)
