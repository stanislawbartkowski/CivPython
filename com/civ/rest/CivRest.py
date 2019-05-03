'''
Created on 31 sty 2019

@author: civ
'''
import requests
import json

#SERVERHOST="localhost"
#APPNAME="CIvilizationUI"

SERVERHOST = "think"
APPNAME = "civilization"


class CivError(Exception): 
  
    # Constructor or Initializer 
    def __init__(self, err, errmess):
        self.err = err 
        self.errmess = errmess
  
    # __str__ is to print() the value 
    def __str__(self): 
        return(self.err + " " + self.errmess) 


def __getRestURL():
    return "http://" + SERVERHOST + ":8080/" + APPNAME + "/rest"


def __getText(r):
    if r.status_code == 204 : return ""
    if r.status_code != 200 : raise(CivError("Error while reading REST data", str(r.content)))
    return r.text


def __getRest(url):
    r = requests.get(url)
    return __getText(r)


def __getRestCivData(what, param=None):
    if param == None : url = __getRestURL() + "/civdata?what=" + str(what)
    else : url = __getRestURL() + "/civdata?what=" + str(what) + "&param=" + param
    return __getRest(url)
    
    
def twoPlayersGame(civs):
    return __getRestCivData(6, civs)


def twoPlayersGameWithAutom(civs):
    return __getRestCivData(8, civs)    

                
def singlePlayerGame(civ):        
    r = __getRestCivData(9, civ)
    a = r.split(",")
    # return (token, gameid)
    return (a[0], a[1])


def getCivResource():
    return json.loads(__getRestCivData(0))


def registerAutom():
    url = __getRestURL() + "/registerautom?autom=" + "true"
    r = requests.put(url)
    # code 204, no contents, expected here
    __getText(r)

    
def getGameid():
    url = __getRestURL() + "/getwaiting"
    return __getRest(url)        


def getWaitingGames():
    return json.loads(__getRestCivData(5))


def findGame(games, gameid):
    for e in games :  
        if e["gameid"] == int(gameid) : return e["waiting"][0]
    raise(CivError(gameid, "Cannot find the game in the waiting list"))


def joinGame(gameid, civ):
    url = __getRestURL() + "/joingame?gameid=" + gameid + "&civ=" + civ
    r = requests.post(url)
    return __getText(r)


def getBoard(token):
    return json.loads(__getRestCivData(2, token))


def itemizeCommand(token, command):
    url = __getRestURL() + "/itemize?token=" + token + "&command=" + command
    return json.loads(__getRest(url))


def deleteGame(gameid):
    url = __getRestURL() + "/delete?gameid=" + gameid
    r = requests.delete(url)
    __getText(r)

    
def unregisterG(token):
    __getRestCivData(4, token)        

    
def executeCommand(token, action, row, col, jsparam=None):
    url = __getRestURL() + "/command?token=" + token + "&action=" + action + "&row=" + str(row) + "&col=" + str(col)
    if jsparam != None: url = url + "&jsparam=" + jsparam
    r = requests.post(url)
    res = __getText(r)
    if res != None and res != "" : raise(CivError(action, res))

def __postJson(rest, js, civ):
    url = __getRestURL() + "/" + rest + "?civ=" + civ
    r = requests.post(url, data=js)
    return __getText(r)

    
def postsingleGame(js, civ):
    return __postJson("deploygame", js, civ)    

