'''
Created on 10 maj 2019

@author: civ
'''
import unittest

from com.civ.rest import CivRest as C
from com.civ.commands import Commands as CO
from com.civ.play.Play import getSquare,getPlayerTrade,getPlayerCards,getPlayerGreatPersons,getPlayerResourceN,getPlayerHutVillages
from com.civ.play import misc
from com.civ.commands import Resources as RE

from helper import TestHelper

class Test6(unittest.TestCase):

    def setUp(self):
        C.registerAutom()


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




