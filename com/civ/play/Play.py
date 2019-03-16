'''
Created on 1 lut 2019

@author: civ
'''

from com.civ.rest import CivRest as C
from com.civ.commands import Commands as CO
import random
from com.civ.play import misc
import json

random.seed()


def buildCity(P) :
    # print(P.i)
    # choose random
    pos = misc.getRandom(P.i)
    assert (pos != None)
    # print (pos)
    P.executeCommandP(pos)

    
def deployFigure(P): 
    print(P.i)
    # choose random city and point
    city = misc.getRandom(P.i)
    # get random square
    c = city["p"]
    point = city["param"]
    P.executeCommandPP(c, point)

    
def buyUnit(P):
    print(P.i)    
    # choose random city
    city = misc.getRandom(P.i)
    c = city["p"]
    P.executeCommandP(c)

    
def startMove(P, selfun):
    P.visited = None
    f = misc.getRandom(P.i, selfun)
    P.executeCommandPP(f['p'], f['f'])

    
def onList(p, l):
    for i in l :
        if misc.eqP(i, p) : return True
    return False    


def endOfMove(P):
    P.co = CO.Command.ENDOFMOVE
    P.executeCommand()    

    
def move(P, selfun):
    if P.visited == None : P.visited = []
    
    moved = []
    key = 'moves'
    if P.co == CO.Command.EXPLOREHUT : key = "explore"
    for i in P.i[key] :
        if not onList(i, P.visited) : 
            moved.append(i)
    
    if len(moved) == 0 :
        endOfMove(P)
        return
    
    m = misc.getRandom(moved, selfun)
    P.visited.append(m)
    P.executeCommandP(m)

    
def revealTile(P) :
    l = P.i["tiles"]
    # can be more then 1 tile to reveal
    r = misc.getRandom(l)    
    P.executeCommandPP(r["p"], r["orientation"])

    
def endOfPhase(P):
    P.co = CO.Command.ENDOFPHASE
    phase = P.b["board"]["game"]["phase"]
    P.executeCommandJ(phase)

    
def researchTechnology(P):
    tech = misc.getRandom(P.i)
    P.executeCommandJ(tech)

def harvestResource(P):
    pair = misc.getRandom(P.i)
    P.executeCommandPP(pair["p"],pair["param"])       

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
        commands = self.b['board']['you']['commands']
        # remove not supported yet
        comm = []
        endof = None
        for c in commands :
            co = CO.toCommand(c['command'])
            if co == None : continue
            if co == CO.Command.ENDOFMOVE or co == CO.Command.ENDOFPHASE :
                endof = co 
                continue
            comm.append(co)
        if len(comm) == 0 and endof != None : return [endof]
        return comm
        
    def __chooseCommand(self):     
        comm = self.getCommands()
        return misc.getRandom(comm)
    
    def playSingleCommand(self, co, selfun=None):
        self.co = co
        if co == CO.Command.ENDOFMOVE : self.i = []
        else : self.i = C.itemizeCommand(self.token, CO.toS(self.co))
        if self.co == CO.Command.SETCAPITAL : 
            buildCity(self)
            return True
        if self.co == CO.Command.SETSCOUT or self.co == CO.Command.SETARMY or self.co == CO.Command.BUYSCOUT or self.co == CO.Command.BUYARMY :
            deployFigure(self)
            return True
        if self.co == CO.Command.BUYAIRCRAFT or self.co == CO.Command.BUYARTILLERY or self.co == CO.Command.BUYINFANTRY or self.co == CO.Command.BUYMOUNTED :
            buyUnit(self)
            return True
        if self.co == CO.Command.STARTMOVE :
            startMove(self, selfun)
            return True
        if self.co == CO.Command.MOVE or self.co == CO.Command.EXPLOREHUT:
            move(self, selfun)
            return True
        if self.co == CO.Command.ENDOFMOVE:
            endOfMove(self)
            return True
        if self.co == CO.Command.REVEALTILE :
            revealTile(self)
            return True
        if self.co == CO.Command.ENDOFPHASE :
            endOfPhase(self)
            return True
        if self.co == CO.Command.RESEARCH :
            researchTechnology(self)
            return True
        if self.co == CO.Command.HARVESTRESOURCE :
            harvestResource(self)
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
        
    def deleteGame(self):
        if self.tokena : C.unregisterG(self.tokena)
        if self.tokenb : C.unregisterG(self.tokenb)
        C.deleteGame(self.gameid)
        
