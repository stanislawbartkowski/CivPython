'''
Created on 16 lut 2019

@author: civ
'''
import unittest

from com.civ.rest import CivRest as C
from com.civ.commands import Commands as CO

from helper import TestHelper


class Test2(unittest.TestCase):

    def setUp(self):
        C.registerAutom()
        
    def __playc(self, co):
        G = TestHelper.DeployTestGame("test1", "game-1.json", "America")
        PA = G.playA()
        PA.playSingleCommand(co)
        PA.readBoard()
        return (G, PA)

    def __runUnit(self, co, name):
        (G, PA) = self.__playc(co)
        TestHelper.verifyNumOfUnits(self, PA.b, name, 2)
        G.deleteGame()
        
#    @unittest.skip("demonstrating skipping")
    def test1(self):
        self.__runUnit(CO.Command.BUYINFANTRY, "Infantry")
        self.__runUnit(CO.Command.BUYMOUNTED, "Mounted")
        self.__runUnit(CO.Command.BUYARTILLERY, "Artillery")
        
    def test2(self):
        (G, PA) = self.__playc(CO.Command.BUYARMY)
        TestHelper.verifyNumberOfFigures(self, PA.b, "armieslimit", 4)
        G.deleteGame()

