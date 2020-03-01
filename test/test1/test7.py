'''
Created on 10 maj 2019

@author: civ
'''
import unittest

from com.civ.rest import CivRest as C
from com.civ.commands import Commands as CO
from com.civ.play.Play import getPlayerTrade,getBattle,getPlayerResourceN,playBattle,playTwoBattle,endOfGame,getSuspend,getUnitList,playSuspend
from com.civ.commands import Resources as RE
from com.civ.play.Play import TestGame


from helper import TestHelper

class Test7(unittest.TestCase):

    def setUp(self):
        TestHelper.startTest()
        
#    @unittest.skip("demonstrating skipping")
    def test1(self):
        print("Cannot stop in water")
        G = TestHelper.DeployTestGame("test1", "game-71.json", "China,Rome")
        # Rome
        PB = G.playB()
        PB.readBoard()
        # next move
        PB.playCommand()
        # read again
        PB.readBoard()
#        PB.playSingleCommand(CO.Command.ENDOFMOVE)
        
        PB.playCommand()
        
        PB.readBoard()        
        PB.playCommand()
        
        G.deleteGame()

    def test2(self):
        print("Initialize game and resume")
        G = TestGame()
        G.registerSingleGame("China")
        gameid = G.gameid
        print("gameid=" + gameid)
        G.resumeGame(gameid,"China")
        PA = G.playA()
        PA.readBoard()
        G.deleteGame()





        
    

