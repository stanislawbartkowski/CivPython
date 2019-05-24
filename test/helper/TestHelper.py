'''
Created on 16 lut 2019

@author: civ
'''

import os
from pathlib import Path
from com.civ.play.Play import TestGame


def readJsonFile(test, fname):
    c = os.path.dirname(os.path.abspath(__file__))
    fname = os.path.join(c, "../resource/", test, fname)
    content = Path(fname).read_text()
    return content


def DeployTestGame(test, fname, civ):
    g = TestGame()
    board = readJsonFile(test, fname)
    a = civ.split(",")
    if len(a) == 1: g.deploySingleGame(board, civ)
    else : g.deployTwoGame(board, civ)
    return g


def verifyNumOfUnits(te, b, name, expectedno):
    u = b['board']['you']['units']['units']
    for un in u :
        if un['name'] == name :
            no = un['num']
            te.assertEqual(no, expectedno)
            return
    te.fail("Internal error, cannot find " + name)

    
def verifyNumberOfFigures(te, b, name, expectedno):
    no = b['board']['you'][name]
    te.assertEqual(no, expectedno)
