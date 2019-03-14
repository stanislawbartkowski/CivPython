'''
Created on 1 lut 2019

@author: civ
'''

from com.civ.rest import CivRest as C
import random
from com.civ.play import misc
from com.civ.play.Play import Play


def registerNewGame():
    return C.twoPlayersGameWithAutom("China,Rome")


def play(P):
    P.readBoard()
    while P.playCommand() : P.readBoard()


if __name__ == '__main__':
    random.seed()
    try :
        C.registerAutom()
        tokena = registerNewGame()
        tokenb = misc.joinGame()
        PA = Play(tokena)
        PB = Play(tokenb)
        play(PA)
    except Exception as e :
        print(e)
        
