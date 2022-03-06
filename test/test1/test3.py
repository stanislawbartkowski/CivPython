'''
Created on 26 lut 2019

@author: civ
'''
import unittest

from com.civ.rest import CivRest as C
from com.civ.play.Play import TestGame
from com.civ.commands import Commands as CO
from com.civ.play import misc
from com.civ.play.Types import *

from helper import TestHelper


class Test(unittest.TestCase):

    def setUp(self):
        C.registerAutom()
        
    def _run(self):
        G = TestHelper.DeployTestGame("test1", "game-32.json", "America")
        PA = G.playA()
        PA.readBoard()
        p : Point = Point.initp(2,2)
        PA.playSingleCommand(CO.Command.STARTMOVE, lambda x : p == x['p'])
        PA.readBoard()
        p : Point = Point.initp(2,1)
        PA.playSingleCommand(CO.Command.MOVE, lambda x : p == x)
        PA.readBoard()
        p : Point = Point.initp(1,1)
        PA.playSingleCommand(CO.Command.MOVE, lambda x : p ==  x)
        PA.readBoard()
        return (G, PA)
    
    def _playtoPhase(self, PA):
        while True :
            PA.playCommand()
            PA.readBoard()
            comm = PA.getCommands()
            print(comm)
            if comm == [CO.Command.ENDOFPHASE] : break
        # endofphase
        PA.playSingleCommand(CO.Command.ENDOFPHASE)

#    @unittest.skip("demonstrating skipping")
    def test1(self):
        (G, PA) = self._run()
        PA.playSingleCommand(CO.Command.ENDOFMOVE)
        PA.readBoard()
        comm = PA.getCommands()
        print(comm)
        self.assertFalse(CO.Command.ENDOFMOVE in comm)
        self.assertFalse(CO.Command.MOVE in comm)
        self.assertTrue(CO.Command.STARTMOVE in comm)
        G.deleteGame()

#    @unittest.skip("demonstrating skipping")
    def test2(self):
        (G, PA) = self._run()
        # should issue automatically ENDOFMOVE
        PA.playCommand()
        PA.readBoard()
        comm = PA.getCommands()
        print(comm)
        self.assertFalse(CO.Command.ENDOFMOVE in comm)
        self.assertFalse(CO.Command.MOVE in comm)
        self.assertTrue(CO.Command.STARTMOVE in comm)
        G.deleteGame()
        
    @unittest.skip("demonstrating skipping")
    # TODO: test fails, requires further investigation
    def test3(self):
        (G, PA) = self._run()
        # wait until endofphase
        self._playtoPhase(PA)
        # check now
        PA.readBoard()
        comm = PA.getCommands()
        print(comm)
        self.assertTrue(CO.Command.RESEARCH in comm)
        G.deleteGame()
        
    @unittest.skip("demonstrating skipping")
    # TODO: test fails, requires further investigation
    def test4(self):
        (G, PA) = self._run()
        # wait until endofphase
        self._playtoPhase(PA)
        PA.readBoard()
        # execute research
        PA.playSingleCommand(CO.Command.RESEARCH)
        PA.readBoard()
        comm = PA.getCommands()
        print(comm)
        G.deleteGame()
        
    def test5(self):
        G = TestHelper.DeployTestGame("test1", "game-35.json", "America")
        PA = G.playA()
        PA.readBoard()
        comm = PA.getCommands()
        print(comm)
        self.assertTrue(CO.Command.EXPLOREHUT in comm)
        p : Point = Point.initp(0,4)
        PA.playSingleCommand(CO.Command.EXPLOREHUT,lambda x : p ==  x)
        G.deleteGame()

