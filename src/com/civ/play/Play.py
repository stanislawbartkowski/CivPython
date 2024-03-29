'''
Created on 1 lut 2019

@author: civ
'''

from typing import List, Callable
from com.civ.rest import CivRest as C
from com.civ.commands import Commands as CO
from com.civ.commands import Resources as RE
import random
from com.civ.play import misc
from com.civ.play.Types import *
import json
import logging

random.seed()

# ---------------------------
# board related methods
# ---------------------------

def _getB(P):
    return P.b["board"]

def _getYou(P):
    return _getB(P)['you']

def _getCiv(P):
    return _getYou(P)['civ']

def _getOther(P):
    l = _getB(P)['others']
    if len(l) : return l[0]
    return None
    
def _getMap(P):
    return _getB(P)["map"]

def getUnitList(P):        
    return _getYou(P)["units"]["list"]

def getSquare(P,row,col):
    map = _getMap(P)
    s = map[row][col]
    return s

def getResources(P):
    return _getB(P)["resources"]

def getPlayerCards(P):
    return _getYou(P)["cultureresource"]["cards"]

def getPlayerGreatPersons(P):
    return _getYou(P)["cultureresource"]["persons"]

def _getPlayerResources(P):
    return _getYou(P)["resources"]

def getSuspend(P):
    return _getYou(P)["suspended"]   

def _getRN(rr,r) :
    s = RE.toS(r)
    for r in rr :
        if r["resource"] == s : return r["num"]
    raise Exception('Resource does not exist in the board ot player resource list', r)

''' Get number of a particular resource on the player panel
    Parameters:
      P : player panel
      r : resource name (enumeration)
    Returns: number of resources
'''
def getPlayerResourceN(P,r):
    rr =  _getPlayerResources(P)
    return _getRN(rr,r)

''' Get number of a particular resource on board
    Parameters:
      P : player panel
      r : resource name (enumeration)
    Returns: number of resources
'''
def getResourceN(P,r):
    rr =  getResources(P)
    return _getRN(rr,r)

def endOfGame(P):
    return _getB(P)["endofgame"]

def cultureProgress(P):
    y = _getYou(P)['cultureprogress']
    return y

def getPlayerTrade(P):
    t = _getYou(P)['trade']
    return t

def _getPlayerTradeForProd(P):
    t = _getYou(P)['tradeforprod']
    return t

def getPlayerHutVillages(P):
    t = _getYou(P)["hutvillages"]['list']
    return t
    
def getBattle(P):
    bo = _getB(P)
    return bo['battle']    

# -------------------------
# supporting methods
# -------------------------

def onList(p : Point, l : List[Point]) -> bool:
##    for i in l :
##        if misc.eqP(i, p) : return True
##    return False    
    return p in l

# ----------------------
# commands
# ----------------------

def _buildCity(P) :
    # print(P.i)
    # choose random
    pos = misc.getRandom(P.i)
    assert (pos != None)
    # print (pos)
    P.executeCommandP(pos)

    
def _deployFigure(P): 
#    print(P.i)
    # choose random city and point
    city = misc.getRandom(P.i)
    # get random square
    c = city["p"]
    point = city["param"]
    P.executeCommandPP(c, point)

    
def _buyUnit(P):
#    print(P.i)    
    # choose random city
    city = misc.getRandom(P.i)
    c = city["p"]
    P.executeCommandP(c)

# Figures movement
    
def _startMove(P, selfun) -> None:
    P.visited = None
    fig = misc.getRandom(P.i, selfun)
    
    f : Figures
    p : Point
    p, f = Point(fig['p']),Figures(fig['f'])
    
    P.executeTCommandPP(p, f)

def _endOfMove(P):
    P.co = CO.Command.ENDOFMOVE
    P.executeCommand()    

    
def _move(P, selfun : Callable):
    if P.visited == None : P.visited = []
    
    moved : List[Point] = []
    key = 'moves'
    if P.co == CO.Command.EXPLOREHUT : key = "explore"
    list = P.i[key]

    moved = [ Point(i) for i in list if not i in P.visited ] 
    
    if len(moved) == 0 :
        _endOfMove(P)
        return
    
    m : Point = misc.getRandom(moved, selfun)
    P.visited.append(m)
    P.executeTCommandP(m)

# ===================
    
def _revealTile(P) :
    l = P.i["tiles"]
    # can be more then 1 tile to reveal
    r = misc.getRandom(l)    
    P.executeCommandPP(r["p"], r["orientation"])
    
def _endOfPhase(P):
    P.co = CO.Command.ENDOFPHASE
    phase = _getB(P)["game"]["phase"]
    P.executeCommandJ(phase)
    
def _researchTechnology(P):
    tech = misc.getRandom(P.i)
    P.executeCommandJ(tech)

def _harvestResource(P):
    pair = misc.getRandom(P.i)
    P.executeCommandPP(pair["p"],pair["param"])
    
def _sendProduction(P) :
    f = misc.getRandom(P.i)
    P.executeCommandPP(f['p'],f['param'])
    
def _buyBuilding(P,key,selfun,selfun1):
    city = misc.getRandom(P.i,selfun)
    building = misc.getRandom(city["list"],selfun1)
    P.executeCommandPP(city['p'],{ "p" : building["p"],key : building[key]})
    
def _devottoCluster(P) :
    city = misc.getRandom(P.i)
    P.executeCommandPP(city['p'],city['list'])
    
def _doAction(P):
    P.executeCommand()    
    
def _spendTrade(P,selfun,param):
    city = misc.getRandom(P.i,selfun)
    if param == None :
        # calculate random
        no = int(getPlayerTrade(P)/_getPlayerTradeForProd(P))
        # int() calculates prod
        param = misc.getRandomNo(no) + 1
        # calculate random from 0 to no
    P.executeCommandPP(city['p'],param)
    
def _discardCard(P):
    card = misc.getRandom(P.i)
    P.executeCommandJ(card)
    
def _selectHV(P,hv,resource):
    t = getPlayerHutVillages(P)
    s = RE.toHVS(hv)
    matches = [x for x in t if x['hv'] == s and x['resource'] == resource]
    return matches

def _selectMarketRes(P,resource):
    no = getPlayerResourceN(P, resource)
    if no == 0 : return None
    return {"resource" : RE.toS(resource)}
    
    
def _selectResource(P,resource):
    rs = RE.toS(resource)
    # select hut and resource
    m = _selectHV(P, RE.HV.HUT,rs)
    res = misc.getRandom(m)
    if res : return res
    # market
    res = _selectMarketRes(P, resource)
    if res : return res
    # select village
    m = _selectHV(P, RE.HV.VILLAGE,rs)
    return misc.getRandom(m)            
    
def _currencyAction(P) :
    res = _selectResource(P, RE.Resource.INCENSE)
    P.executeCommandJ(res)
    
def _useSilkAction9(P):
    res = _selectResource(P, RE.Resource.SILK)
    # select side receiving 6 silk
    o = _getOther(P)
    if o : P.executeCommandJ({"resource" : res, "civ" : o['civ']})
    else : P.executeCommandJ({"resource" : res})
    
def _attack(P):
    l = P.i['attack']
    res = misc.getRandom(l)
    P.executeCommandP(res)
    
def _playUnit(P):
    ba = getBattle(P)
    at = ba['attacker']
    de = ba['defender']
    # turn in attacker and defender excludes themselves    
    if at['turn'] : am = at
    else : am = de
    if not am['you'] : return False
    # am - army making attack now
    (_,fro) = misc.getRandomI(am['waiting']['list'])    
    # get random unit from standing units
    f = am['front']
    # list of empty slots
    slots = list(filter( lambda x : f[x] == None, list(range(0,len(f)))))
    to = misc.getRandom(slots)
    P.co = CO.Command.PLAYUNIT
    P.executeCommand(fro,to)
    return True

def _endOfBattle(P):
    P.readBoard()
    b = getBattle(P)
    return b["endofbattle"]

def playSuspend(P) :
    # suspend or anul
    ra = misc.getRandomNo(2)
    # 50 % 
    if ra == 0 :
        P.doCommand(CO.Command.LETSUSPENDEDGO)
        return
    # anul action
    su = getSuspend(P)
    li = su["list"]
    # list of action to use
    ac = misc.getRandom(li)
    P.doCommandS(ac["command"])
    
def playBattle(P):
    while not _endOfBattle(P) : _playUnit(P)    
    P.playSingleCommand(CO.Command.ENDBATTLE)
    
    
def playTwoBattle(PA,PB):
    
    while True:
        if _endOfBattle(PA) : break
        if _playUnit(PA) : continue
        if _endOfBattle(PB) : break
        _playUnit(PB)
        
    PB.readBoard()
    # identify the winner
    b = getBattle(PA)
    if b['attackerwinner'] : civ = b['attacker']['civ']
    else : civ = b['defender']['civ']
    if _getCiv(PA) == civ : PA.playSingleCommand(CO.Command.ENDBATTLE)
    else : PB.playSingleCommand(CO.Command.ENDBATTLE)
    
def _winnerLoot(P):
    l = getBattle(P)['winnerloot']    
    loottotake = l['loot']
    li = l['list']
    loot = []
    while True :
        # collect list of loots affordable (list of indexes)
        alist = list(filter( lambda i : li[i]['loot'] <=loottotake, list(range(0,len(li)))))
        if len(alist) == 0 : break
        # take random loot
        ll = misc.getRandom(alist)
        # add to list
        loot.append(li[ll])
        # decrease the loot
        loottotake = loottotake - li[ll]['loot']
        li.pop(ll)
        # next loot
    return loot
 
class Play:

    # player token
    token: str
    bchanged: bool
    
    visited : List[Point]
        
    def __init__(self, token):
        self.token = token
        self.visited = None
        self.bchanged = True

    def doCommandS(self,cos,row=-1,col=-1,jsparam=None) :
        C.executeCommand(self.token, cos, row, col, jsparam)

    def doCommand(self,co,row=-1,col=-1,jsparam=None) :
        C.executeCommand(self.token, CO.toS(co), row, col, jsparam)
        
    def executeCommand(self, row=-1 , col=-1, jsparam=None):
        self.doCommand(self.co, row, col, jsparam)
                
    def executeCommandJ(self, jsparam):
        self.executeCommand(-1, -1, json.dumps(jsparam))        
        
    def executeCommandP(self, p, jsparam=None):
        self.executeCommand(p['row'], p['col'], jsparam)
        
    def executeCommandPP(self, p, pp):
        self.executeCommandP(p, json.dumps(pp))
        
        
    # --- typing ----
    def executeTCommandP(self, p : Point, jsparam : str=None):
        self.executeCommand(p.row, p.col, jsparam)
    
    def executeTCommandPP(self, p : Point, pp : CivO):
        self.executeTCommandP(p, pp.dumpj())
        
    def executeCommandTJ(self, pp : CivO):
        self.executeCommand(-1, -1, pp.dumpj())        

    
        
    def boardChanged(self):
        return self.bchanged

    def readBoard(self):
        b = C.getBoard(self.token)
        # can be empty if nothing has changed
        # leave the previous board
        self.bchanged = b != None
        if b : self.b = b
        
    def getCommands(self):
        commands = _getYou(self)['commands']
        # remove not supported yet
        comm = []
        endof = None
        for c in commands :
            if not CO.isCommand(c['command']) : continue
            co = CO.toCommand(c['command'])
            if co == CO.Command.ENDOFMOVE or co == CO.Command.ENDOFPHASE :
                endof = co 
                continue
            comm.append(co)
        if len(comm) == 0 and endof != None : return [endof]
        return comm
        
    def __chooseCommand(self):     
        comm = self.getCommands()
        return misc.getRandom(comm)
        
    def playSingleCommand(self, co, selfun=None,selfun1=None,param=None):
        self.co = co
        logging.info(_getCiv(self) + " " + str(co))
        if co == CO.Command.ENDOFMOVE or co == CO.Command.PLAYUNIT or co == CO.Command.PLAYUNITIRON or co == CO.Command.ENDBATTLE: self.i = []
        else : self.i = C.itemizeCommand(self.token, CO.toS(self.co))
        if self.co == CO.Command.SETCAPITAL : 
            _buildCity(self)
            return True
        if self.co == CO.Command.SETSCOUT or self.co == CO.Command.SETARMY or self.co == CO.Command.BUYSCOUT or self.co == CO.Command.BUYARMY :
            _deployFigure(self)
            return True
        if self.co == CO.Command.BUYAIRCRAFT or self.co == CO.Command.BUYARTILLERY or self.co == CO.Command.BUYINFANTRY or self.co == CO.Command.BUYMOUNTED :
            _buyUnit(self)
            return True
        if self.co == CO.Command.STARTMOVE :
            _startMove(self, selfun)
            return True
        if self.co == CO.Command.MOVE or self.co == CO.Command.EXPLOREHUT:
            _move(self, selfun)
            return True
        if self.co == CO.Command.ENDOFMOVE:
            _endOfMove(self)
            return True
        if self.co == CO.Command.REVEALTILE :
            _revealTile(self)
            return True
        if self.co == CO.Command.ENDOFPHASE :
            _endOfPhase(self)
            return True
        if self.co == CO.Command.RESEARCH :
            _researchTechnology(self)
            return True
        if self.co == CO.Command.HARVESTRESOURCE :
            _harvestResource(self)
            return True
        if self.co == CO.Command.SENDPRODUCTION :
            _sendProduction(self)
            return True
        if self.co == CO.Command.BUYBUILDING :
            _buyBuilding(self,"building",selfun,selfun1)
            return True
        if self.co == CO.Command.BUYWONDER :
            _buyBuilding(self,"wonder",selfun,selfun1)
            return True
        if self.co == CO.Command.GREATPERSONPUT or self.co == CO.Command.GREATPERSONPUTNOW:
            _buyBuilding(self,"greatperson",selfun,selfun1)
            return True
        if self.co == CO.Command.DEVOUTTOCULTURE:
            _devottoCluster(self)
            return True
        if self.co == CO.Command.ADVANCECULTURE or self.co == CO.Command.GREATPERSONPUTNOWRESIGN :
            _doAction(self)
            return True
        if self.co == CO.Command.SPENDTRADE:
            _spendTrade(self,selfun,param)
            return True
        if self.co == CO.Command.DISCARDCARD :
            _discardCard(self)
            return True
        if self.co == CO.Command.CURRENCYACTION :
            _currencyAction(self)
            return True
        if self.co == CO.Command.USESILKFORTRADE9 :
            _useSilkAction9(self)
            return True
        if self.co == CO.Command.ATTACK :
            _attack(self)
            return True
        if self.co == CO.Command.PLAYUNIT or self.co == CO.Command.PLAYUNITIRON :
            _playUnit(self)
            return True    
        if self.co == CO.Command.ENDBATTLE : 
            self.executeCommandJ(_winnerLoot(self))
            return True    
        return False
    
        
    def playCommand(self):
        co = self.__chooseCommand()
        if co == None : return False
        return self.playSingleCommand(co)
        
        
class TestGame :
     
    def __init__(self):
        self.tokena = None
        self.tokenb = None
        
    def deploySingleGame(self, board, civ):
        a = C.postsingleGame(board, civ).split(',')
        self.tokena = a[0]
        self.gameid = a[1]
        self.tokenb = None

    def deployTwoGame(self, board, civ):
        a = C.postsingleGame(board, civ).split(',')
        self.tokena = a[0]
        self.tokenb = a[1]
        self.gameid = a[2]

                
    def registerSingleGame(self, civ):
        a = C.singlePlayerGame(civ)
        self.tokena = a[0]
        self.gameid = a[1]
        
    def registerTwoGames(self, civs):
        self.tokena = C.twoPlayersGameWithAutom(civs)
        (self.tokenb, self.gameid) = misc.joinGame()
        
    def playA(self):
        return Play(self.tokena)
        
    def playB(self):
        return Play(self.tokenb)
    
    def _play(self, P,PO = None):
        P.readBoard()
        while True :
            if endOfGame(P) : return False 
            if getSuspend(P) :
                playSuspend(P)
            else:
                if getBattle(P) :
                    playTwoBattle(P, PO)
                else:
                    if not P.playCommand() : return True 
            P.readBoard()

    def playN(self, P,no):
        P.readBoard()
        for i in range(no) :                
            if not P.playCommand(): break 
            P.readBoard()

    def unregisterToken(self) :
        if self.tokena : C.unregisterG(self.tokena)
        if self.tokenb : C.unregisterG(self.tokenb)

    def deleteGame(self):
        self.unregisterToken()
        C.deleteGame(self.gameid)

    def resumeGame(self,gameid,civ):
        a = C.resumeGame(gameid,civ).split(',')
        self.tokena = a[0]
        self.gameid = a[1]
        self.tokenb = None
        
    def playGameToEnd(self):
        PA = self.playA()
        PB = self.playB()        
        while True:
            print("loop")
            if not self._play(PA,PB) : 
                return
            if not self._play(PB,PA) : 
                return