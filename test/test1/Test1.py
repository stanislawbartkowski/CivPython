'''
Created on 3 lut 2019

@author: civ
'''
import unittest

from com.civ.rest import CivRest as C
from com.civ.play.Play import TestGame

from helper import TestHelper


class Test(unittest.TestCase):
    
    def setUp(self):
        C.registerAutom()

#    @unittest.skip("demonstrating skipping")
    def test1(self):
        print("Simple test for single player game")
        G = TestGame()
        G.registerSingleGame("China")
        P = G.playA()
        G.play(P)
        G.deleteGame()

    @unittest.skip("demonstrating skipping")        
    def test2(self):
        print("Simple test for two player game")
        G = TestGame()
        G.registerTwoGames("China,Rome")
        PA = G.playA()
        G.play(PA)
        PB = G.playB()
        G.play(PB)
        G.deleteGame()
        
    @unittest.skip("demonstrating skipping")        
    def test3(self):
        print("Deploy game and delete game")
        G = TestHelper.DeployTestGame("test1", "game-1.json", "America")
        G.deleteGame()
        
