'''
Created on 10 maj 2019

@author: civ
'''
import unittest

from com.civ.rest import CivRest as C
from com.civ.commands import Commands as CO
from com.civ.play.Play import getSquare,getPlayerTrade,getBattle,getPlayerGreatPersons,getPlayerResourceN,getPlayerHutVillages,playBattle
from com.civ.play import misc
from com.civ.commands import Resources as RE

from helper import TestHelper

class Test6(unittest.TestCase):

    def setUp(self):
        C.registerAutom()

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
        
        PA.readBoard()

        playBattle(PA)
                
        print("End of battle")
        PA.readBoard()
        b = getBattle(PA)
        print(b)
        self.assertIsNone(b, "Bloodshed stopped")
        
        G.deleteGame()
