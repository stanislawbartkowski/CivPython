'''
Created on 1 maj 2019

@author: civ
'''
import unittest

from com.civ.rest import CivRest as C
from com.civ.commands import Commands as CO
from com.civ.play.Play import getSquare,getPlayerTrade,getPlayerCards,getPlayerGreatPersons
from com.civ.play import misc


from helper import TestHelper

class Test(unittest.TestCase):

    def setUp(self):
        C.registerAutom()

    @unittest.skip("demonstrating skipping")
    def test1(self):
        print("Test SPENDTRADE")
        G = TestHelper.DeployTestGame("test1", "game-51.json", "America")
        PA = G.playA()
        PA.readBoard()
        s = getSquare(PA, 2, 2)
        print(s)
        t = getPlayerTrade(PA)
        print(t)
        self.assertEqual(s['production'],5)
        self.assertEqual(t,7)        
        PA.playSingleCommand(CO.Command.SPENDTRADE,lambda x : misc.eqP({"row" : 2, "col" : 2}, x['p']),param=3)
        PA.readBoard()
        s = getSquare(PA, 2, 2)
        print(s)
        print("Production increased to 8")
        self.assertEqual(s['production'],8)
        t = getPlayerTrade(PA)
        print(t)
        print("Trade decreased to 1 (7 - 2 * 3).")
        self.assertEqual(t,1)
        G.deleteGame()

    @unittest.skip("demonstrating skipping")
    def test2(self):
        print("Test ADVANCECULTURE and DROPCARD")
        G = TestHelper.DeployTestGame("test1", "game-52.json", "America")
        PA = G.playA()
        PA.readBoard()
        # single city
        PA.playSingleCommand(CO.Command.DEVOUTTOCULTURE)
        PA.readBoard()
        PA.playSingleCommand(CO.Command.ADVANCECULTURE)
        PA.readBoard()        
        cards = getPlayerCards(PA)
        self.assertEqual(len(cards),3)
        PA.playSingleCommand(CO.Command.DISCARDCARD)
        PA.readBoard()        
        cards = getPlayerCards(PA)
        print("One card less, 2 expected")
        self.assertEqual(len(cards),2)
        G.deleteGame()

    @unittest.skip("demonstrating skipping")
    def test3(self):
        print("Test BUYWONDER")
        G = TestHelper.DeployTestGame("test1", "game-53.json", "America")
        PA = G.playA()
        PA.readBoard()
        PA.playSingleCommand(CO.Command.BUYWONDER,lambda x : misc.eqP({"row" : 2, "col" : 2}, x['p']),
                                                  lambda b : misc.eqP({"row" : 1, "col" : 1}, b['p']) and b['wonder'] == "TheColossus")
        PA.readBoard()
        s = getSquare(PA, 1,1)
        print(s)
        print("TheCollosus is expected to be there")
        self.assertEqual(s["wonder"], "TheColossus")
        G.deleteGame()
        
    @unittest.skip("demonstrating skipping")
    def test4(self):
        print("Test BUYWONDER")
        G = TestHelper.DeployTestGame("test1", "game-54.json", "America")
        PA = G.playA()
        PA.readBoard()
        PA.playSingleCommand(CO.Command.GREATPERSONPUT,lambda x : misc.eqP({"row" : 2, "col" : 2}, x['p']),
                                                  lambda b : misc.eqP({"row" : 1, "col" : 1}, b['p']) and b['greatperson'] == "AlanTuring")
        PA.readBoard()
        s = getSquare(PA, 1,1)
        print(s)
        print("Scientist is expected here")
        self.assertEqual(s["greatpersontype"], "Scientist")
        G.deleteGame()
        
    @unittest.skip("demonstrating skipping")
    def test6(self):
        print("Advance Culture and put great person on board now")
        G = TestHelper.DeployTestGame("test1", "game-55.json", "America")
        PA = G.playA()
        PA.readBoard()
        PA.playSingleCommand(CO.Command.GREATPERSONPUTNOW,lambda x : misc.eqP({"row" : 2, "col" : 2}, x['p']),
                                                  lambda b : misc.eqP({"row" : 1, "col" : 1}, b['p']) and b['greatperson'] == "LouisPasteur")
        PA.readBoard()
        s = getSquare(PA, 1,1)
        print(s)
        print("Scientist is expected here")
        self.assertEqual(s["greatpersontype"], "Scientist")
        G.deleteGame()
        
    def test7(self):
        print("Advance Culture and keep great person on hold")
        G = TestHelper.DeployTestGame("test1", "game-55.json", "America")
        PA = G.playA()
        PA.readBoard()
        PA.playSingleCommand(CO.Command.GREATPERSONPUTNOWRESIGN)
        g = getPlayerGreatPersons(PA)
        print("Check that LouisPasteur is down the list")
        self.assertIn("LouisPasteur", g) 
        G.deleteGame()
