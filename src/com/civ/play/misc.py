'''
Created on 1 lut 2019

@author: civ
'''

from com.civ.rest import CivRest as C
import random
import json
from typing import List,Tuple, Callable, Dict

def joinGame():
    gameid = C.getGameid()
    games = C.getWaitingGames()
    civwaiting = C.findGame(games, gameid)
    token = C.joinGame(gameid, civwaiting).split(',')[0]
    return (token, gameid)

def getRandomNo(no : int) -> int:
    return random.randrange(0, no)

def getRandomI(a : List[any], selfun : Callable=None) -> Tuple[any,int] :
    if len(a) == 0 : return None,-1
    if selfun == None :
        i = getRandomNo(len(a))
        return a[i],i
    for i in range(len(a)) :
        if selfun(a[i]) : return a[i],i
    return None,-1

def getRandom(a : List[any], selfun : Callable =None) -> Tuple[any,int] :
    (re,_) = getRandomI(a, selfun)
    return re

def eqP(p1 : Dict, p2 : Dict) -> bool :
    return (p1["row"] == p2["row"]) and (p1["col"] == p2["col"])

class MapCR : 
    
    def __init__(self,map):
        self._map = map
        
    def toC(self,k):
        return self._map[k]
    
    def isC(self,k): 
        return self._map.get(k) != None

    def toK(self,val):
        for k,v in self._map.items() : 
            if v == val : return k
        raise Exception('Value does not exist in the map', val)
