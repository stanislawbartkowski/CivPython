'''
Created on 31 sty 2019

@author: civ
'''

import sys
from com.civ.play import misc


print(sys.path)


from com.civ.rest import CivRest as C
import random


def registerNewGame():
    return C.twoPlayersGameWithAutom("China,Rome")


def joinGame():
    (token,_) = misc.joinGame()
    return token

def chooseCommand(b):
    commands = b['board']['you']['commands']
    if len(commands) == 0 : return None
    i = random.randrange(0, len(commands))
    return commands[i]['command']

if __name__ == '__main__':
    random.seed()
    try :
        C.registerAutom()
        tokenp = registerNewGame()
        print(tokenp)
        tokena = joinGame()
        print(tokena)
        b = C.getBoard(tokenp)
        print(b)
        y = b['board']['you']
        print(y)
        co = y['commands']
        print(co)
        comm = chooseCommand(b)
        print(comm)
        item = C.itemizeCommand(tokena, comm)
        print(item)        
    except Exception as e :
        print(e)
