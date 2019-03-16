'''
Created on 16 mar 2019

@author: civ
'''
import unittest

from com.civ.rest import CivRest as C
from com.civ.play.Play import TestGame
from com.civ.commands import Commands as CO
from com.civ.play import misc

from helper import TestHelper




class Test(unittest.TestCase):

    def setUp(self):
        C.registerAutom()


    def test1(self):
        G = TestHelper.DeployTestGame("test1", "game-41.json", "America")
        PA = G.playA()
        PA.readBoard()
        PA.playSingleCommand(CO.Command.HARVESTRESOURCE)
        PA.readBoard()
        comm = PA.getCommands()
        print(comm)
        self.assertFalse(CO.Command.HARVESTRESOURCE in comm)





