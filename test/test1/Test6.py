'''
Created on 10 maj 2019

@author: civ
'''
import unittest

from com.civ.rest import CivRest as C
from com.civ.commands import Commands as CO
from com.civ.play.Play import getPlayerTrade,getBattle,getPlayerResourceN,playBattle,playTwoBattle,endOfGame
from com.civ.commands import Resources as RE
from com.civ.play.Play import TestGame


from helper import TestHelper

class Test6(unittest.TestCase):

    def setUp(self):
        TestHelper.startTest()

    @unittest.skip("demonstrating skipping")
    def test1(self):
        print("Test SPENDTRADE")
        G = TestHelper.DeployTestGame("test1", "game-61.json", "America")
        PA = G.playA()
        PA.readBoard()
        no = getPlayerResourceN(PA,RE.Resource.SILK)
        print(no)
        print("Silk before:" + str(no))
        self.assertEqual(no,1)
        t1 = getPlayerTrade(PA)
        print("Trade before :" + str(t1))        

        PA.playSingleCommand(CO.Command.USESILKFORTRADE9)
        PA.readBoard()
        
        no = getPlayerResourceN(PA,RE.Resource.SILK)
        print(no)
        print("Silk after:" + str(no))
        self.assertEqual(no,0)
        t2 = getPlayerTrade(PA)
        print("Trade after, increased by 9 :" + str(t2))
        self.assertEqual(t1 + 9,t2)                
        
        G.deleteGame()

    @unittest.skip("demonstrating skipping")
    def test2(self):
        print("Test ATTACK")
        G = TestHelper.DeployTestGame("test1", "game-62.json", "America")
        PA = G.playA()
        PA.readBoard()
        print("No battle expected")
        b = getBattle(PA)
        self.assertIsNone(b)
        
        PA.playSingleCommand(CO.Command.ATTACK)
        PA.readBoard()
        b = getBattle(PA)
        print("Battle expected")
        self.assertIsNotNone(b)

        G.deleteGame()

    @unittest.skip("demonstrating skipping")
    def test3(self):
        print("Test ATTACK and BATTLE")
        G = TestHelper.DeployTestGame("test1", "game-62.json", "America")
        PA = G.playA()
        PA.readBoard()
        b = getBattle(PA)
        print(b)
        self.assertIsNone(b,"No battle yet")
        
        PA.playSingleCommand(CO.Command.ATTACK)
        PA.readBoard()
        b = getBattle(PA)
        print(b)
        self.assertIsNotNone(b,"Now the carnage started...")
        
        # now play unit
        PA.playSingleCommand(CO.Command.PLAYUNIT)
        PA.readBoard()
        self.assertTrue(PA.boardChanged(),"Board has changed")
        
        PA.readBoard()
        self.assertFalse(PA.boardChanged(),"Board has not changed")

        playBattle(PA)
                
        print("End of battle")
        PA.readBoard()
        b = getBattle(PA)
        print(b)
        self.assertIsNone(b, "Bloodshed stopped")
        
        G.deleteGame()

    @unittest.skip("demonstrating skipping")
    def test4(self):
        print("Take loot after battle")
        G = TestHelper.DeployTestGame("test1", "game-64.json", "America,China")
        
        # China can attack
        PB = G.playB()
        PA = G.playA()
        PB.readBoard()
        
        PB.playSingleCommand(CO.Command.ATTACK)        
        PB.readBoard()
        b = getBattle(PB)
        print(b)
        self.assertIsNotNone(b,"Now the battle started...")
        playTwoBattle(PA,PB)
        
        # check end of battle
        PB.readBoard()
        b = getBattle(PB)
        print(b)
        self.assertIsNone(b,"End of battle")
        
        G.deleteGame()
        
    @unittest.skip("demonstrating skipping")        
    def test5(self):
        print("End of game")
        G = TestHelper.DeployTestGame("test1", "game-65.json", "America")
        PA = G.playA()
        PA.readBoard()
        e = endOfGame(PA)
        self.assertIsNone(e, "The show must go on")
        PA.playSingleCommand(CO.Command.ADVANCECULTURE)

        PA.readBoard()
        e = endOfGame(PA)
        print(e)
        self.assertIsNotNone(e, "The end")
        
        
        G.deleteGame()
        
    def test6(self):
        print("Play whole game to the end")
        G = TestGame()
        G.registerTwoGames("China,Rome")
        
        G.playGameToEnd()
        
        G.deleteGame()
        