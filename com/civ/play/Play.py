'''
Created on 1 lut 2019

@author: civ
'''

from com.civ.rest import CivRest as C
from com.civ.commands import Commands as CO
from com.civ.commands import Resources as RE
import random
from com.civ.play import misc
import json

random.seed()

# ---------------------------
# board related methods
# ---------------------------

def _getB(P):
    return P.b["board"]

def _getYou(P):
    return _getB(P)['you']
    
def _getMap(P):
    return _getB(P)["map"]        

def getSquare(P,row,col):
    map = _getMap(P)
    s = map[row][col]
    return s

def getResources(P):
    return _getB(P)["resources"]

def getPlayerCards(P):
    return _getYou(P)["cultureresource"]["cards"]

def _getPlayerResources(P):
    return _getYou(P)["resources"]

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

def cultureProgress(P):
    y = _getYou(P)['cultureprogress']
    return y

def getPlayerTrade(P):
    t = _getYou(P)['trade']
    return t

# -------------------------
# supporting methods
# -------------------------

def onList(p, l):
    for i in l :
        if misc.eqP(i, p) : return True
    return False    

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
    print(P.i)
    # choose random city and point
    city = misc.getRandom(P.i)
    # get random square
    c = city["p"]
    point = city["param"]
    P.executeCommandPP(c, point)

    
def _buyUnit(P):
    print(P.i)    
    # choose random city
    city = misc.getRandom(P.i)
    c = city["p"]
    P.executeCommandP(c)

    
def _startMove(P, selfun):
    P.visited = None
    f = misc.getRandom(P.i, selfun)
    P.executeCommandPP(f['p'], f['f'])


def _endOfMove(P):
    P.co = CO.Command.ENDOFMOVE
    P.executeCommand()    

    
def _move(P, selfun):
    if P.visited == None : P.visited = []
    
    moved = []
    key = 'moves'
    if P.co == CO.Command.EXPLOREHUT : key = "explore"
    for i in P.i[key] :
        if not onList(i, P.visited) : 
            moved.append(i)
    
    if len(moved) == 0 :
        _endOfMove(P)
        return
    
    m = misc.getRandom(moved, selfun)
    P.visited.append(m)
    P.executeCommandP(m)

    
def _revealTile(P) :
    l = P.i["tiles"]
    # can be more then 1 tile to reveal
    r = misc.getRandom(l)    
    P.executeCommandPP(r["p"], r["orientation"])

    
def endOfPhase(P):
    P.co = CO.Command.ENDOFPHASE
    phase = _getB(P)["game"]["phase"]
    P.executeCommandJ(phase)

    
def researchTechnology(P):
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
    
def _advanceCulture(P):
    P.executeCommand()    
    
def _spendTrade(P,selfun,param):
    city = misc.getRandom(P.i,selfun)
    P.executeCommandPP(city['p'],param)
    
def _discardCard(P):
    card = misc.getRandom(P.i)
    P.executeCommandJ(card)        
 
class Play:

    def __init__(self, token):
        self.token = token
        self.visited = None
        
    def executeCommand(self, row=-1 , col=-1, jsparam=None):
        C.executeCommand(self.token, CO.toS(self.co), row, col, jsparam)
        
    def executeCommandJ(self, jsparam):
        self.executeCommand(-1, -1, json.dumps(jsparam))        
        
    def executeCommandP(self, p, jsparam=None):
        self.executeCommand(p['row'], p['col'], jsparam)
        
    def executeCommandPP(self, p, pp):
        self.executeCommandP(p, json.dumps(pp))

    def readBoard(self):
        self.b = C.getBoard(self.token)
        
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
        if co == CO.Command.ENDOFMOVE : self.i = []
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
            endOfPhase(self)
            return True
        if self.co == CO.Command.RESEARCH :
            researchTechnology(self)
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
        if self.co == CO.Command.DEVOUTTOCULTURE:
            _devottoCluster(self)
            return True
        if self.co == CO.Command.ADVANCECULTURE:
            _advanceCulture(self)
            return True
        if self.co == CO.Command.SPENDTRADE:
            _spendTrade(self,selfun,param)
            return True
        if self.co == CO.Command.DISCARDCARD :
            _discardCard(self)
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
    
    def play(self, P):
        P.readBoard()
        while P.playCommand() : P.readBoard()

    def playN(self, P,no):
        P.readBoard()
        for i in range(no) :                
            if not P.playCommand(): break 
            P.readBoard()
        
    def deleteGame(self):
        if self.tokena : C.unregisterG(self.tokena)
        if self.tokenb : C.unregisterG(self.tokenb)
        C.deleteGame(self.gameid)
        
