'''
Created on 26 lut 2019

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
        
    def _run(self):
        G = TestHelper.DeployTestGame("test1", "game-32.json", "America")
        PA = G.playA()
#        PA.playSingleCommand(CO.Command.STARTMOVE, lambda x : (x['p']['row'] == 2 and x['p']['col'] == 2))
        PA.readBoard()
        PA.playSingleCommand(CO.Command.STARTMOVE, lambda x : misc.eqP({"row" : 2, "col" : 2}, x['p']))
        PA.readBoard()
        PA.playSingleCommand(CO.Command.MOVE, lambda x : misc.eqP({"row" : 2, "col" : 1}, x))
        PA.readBoard()
        PA.playSingleCommand(CO.Command.MOVE, lambda x : misc.eqP({"row" : 1, "col" : 1}, x))
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
        PA.playSingleCommand(CO.Command.EXPLOREHUT)        
        G.deleteGame()

