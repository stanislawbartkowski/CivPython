'''
Created on 16 mar 2019

@author: civ
'''
import unittest

from com.civ.rest import CivRest as C
from com.civ.play.Play import TestGame
from com.civ.play.Play import getSquare,getResources,getResourceN,getPlayerResourceN,cultureProgress
from com.civ.commands import Commands as CO
from com.civ.commands import Resources as RE
from com.civ.play import misc

from helper import TestHelper

class Test(unittest.TestCase):

    def setUp(self):
        C.registerAutom()

#    @unittest.skip("demonstrating skipping")
    def test1(self):
        print("Test HARVESTRESOURCE")
        G = TestHelper.DeployTestGame("test1", "game-41.json", "America")
        PA = G.playA()
        PA.readBoard()
        PA.playSingleCommand(CO.Command.HARVESTRESOURCE)
        PA.readBoard()
        comm = PA.getCommands()
        print(comm)
        self.assertFalse(CO.Command.HARVESTRESOURCE in comm)
        G.deleteGame()

#    @unittest.skip("demonstrating skipping")
    def test2(self):
        print("Test SENDPRODUCTION")
        G = TestHelper.DeployTestGame("test1", "game-42.json", "America")
        PA = G.playA()
        PA.readBoard()
        s = getSquare(PA, 2,2)
        print(s)
        self.assertEqual(s["production"], 5)
        PA.playSingleCommand(CO.Command.SENDPRODUCTION)
        PA.readBoard()
        s = getSquare(PA, 2,2)
        print(s)
        self.assertEqual(s["production"], 7)
        G.deleteGame()

#    @unittest.skip("demonstrating skipping")
    def test3(self):
        print("Test BUYBUILDING")
        G = TestHelper.DeployTestGame("test1", "game-43.json", "America")
        PA = G.playA()
        PA.readBoard()
        PA.playSingleCommand(CO.Command.BUYBUILDING,lambda x : misc.eqP({"row" : 2, "col" : 2}, x['p']),
                                                    lambda b : misc.eqP({"row" : 1, "col" : 1}, b['p']) and b['building'] == "Temple")
        print("Check whether Temple is built on (1,1)")
        PA.readBoard()
        s = getSquare(PA, 1,1)
        print(s)                
        self.assertEqual(s["building"], "Temple")
        G.deleteGame()
        
#    @unittest.skip("demonstrating skipping")
    def test4(self):
        print("Test DEVOUTTOCULTURE")
        G = TestHelper.DeployTestGame("test1", "game-44.json", "America")
        PA = G.playA()
        PA.readBoard()
        print(PA.b)
        res = getResources(PA)
        print(res)
        num = getPlayerResourceN(PA,RE.Resource.CULTURE)
        print(num)
        self.assertEqual(num,0)
        PA.playSingleCommand(CO.Command.DEVOUTTOCULTURE)
        # verify
        PA.readBoard()
        num = getPlayerResourceN(PA,RE.Resource.CULTURE)
        print("City was devoted to culture, one culture should drop in")
        print(num)
        self.assertEqual(num,1)
        
        G.deleteGame()
        
    def test5(self):
        print("Test ADVANCECULTURE")
        G = TestHelper.DeployTestGame("test1", "game-45.json", "America")
        PA = G.playA()
        PA.readBoard()
        print(PA.b)
        c = cultureProgress(PA)
        print(c)
        self.assertEquals(c,0)
        PA.playSingleCommand(CO.Command.ADVANCECULTURE)
        # culter should be advanced to 1
        PA.readBoard()
        c = cultureProgress(PA)
        print(c)
        print("Culture should be advanced to 1")
        self.assertEquals(c,1)
        G.deleteGame()
