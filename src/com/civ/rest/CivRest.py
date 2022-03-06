'''
Created on 31 sty 2019

@author: civ
'''

from typing import *
import requests
import json

SERVERHOST="localhost"
#SERVERHOST="thinkde"
PORT="7999"

TOKEN="Token"

class CivError(Exception): 
  
    # Constructor or Initializer 
    def __init__(self, err, errmess):
        super().__init__(err + " " + errmess)
        self.err = err 
        self.errmess = errmess
  

def __getRestURL() -> str:
    return f"http://{SERVERHOST}:{PORT}/rest"


def __getText(r) -> str:
    if r.status_code == 204 : return ""
    if r.status_code != 200 : raise(CivError("Error while reading REST data", str(r.content)))
    return r.text


def __getTokenHeader(token : str) -> Dict :
    return { "Authorization" : TOKEN + " " + token }

def __getRest(url :str ,token : str = None) -> str:
    if token == None : r = requests.get(url)
    else : r = requests.get(url, headers=__getTokenHeader(token))
    return __getText(r)

def __getRestCivData(what : int, param : str =None, token : str =None) -> str :
    if param == None : url = __getRestURL() + f"/civdata?what={what}"
    else : url = __getRestURL() + f"/civdata?what={what}&param={param}"
    return __getRest(url,token)    
    
def twoPlayersGame(civs) -> str:
    return __getRestCivData(6, civs)


def twoPlayersGameWithAutom(civs) -> str :
    return __getRestCivData(8, civs)    

                
def singlePlayerGame(civ : str) -> Tuple :     
    r = __getRestCivData(9, civ)
    a = r.split(",")
    # return (token, gameid)
    return (a[0], a[1])


def getCivResource():
    return json.loads(__getRestCivData(0))


def registerAutom() -> None:
    url = __getRestURL() + "/registerautom?autom=true"
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


def joinGame(gameid : int, civ : str) -> str:
    url = __getRestURL() + f"/joingame?gameid={gameid}&civ={civ}"
    r = requests.post(url)
    return __getText(r)


def getBoard(token):
    te = __getRestCivData(2, token=token)
    # can be empty if nothing has changed since previous getBoard
    if te == "" : return None
    return json.loads(te)


def itemizeCommand(token, command):
    url = __getRestURL() + f"/itemize?command={command}"
    return json.loads(__getRest(url,token=token))

def deleteGame(gameid : int) -> None:
    url = __getRestURL() + f"/delete?gameid={gameid}"
    r = requests.delete(url)
    __getText(r)

    
def unregisterG(token: str) -> None:
    __getRestCivData(4, token=token)        
    
def executeCommand(token : str, action : str, row : int, col : int , jsparam:str =None) -> None:
    url = __getRestURL() + f"/command?action={action}&row={row}&col={col}"
    if jsparam is not None : url += f"&jsparam={jsparam}"
    r = requests.post(url,headers=__getTokenHeader(token))
    res = __getText(r)
    if res != None and res != "" : raise(CivError(action, res))

def __postJson(rest, js, civ):
    url = __getRestURL() + f"/{rest}?civ={civ}"
    r = requests.post(url, data=js)
    return __getText(r)

    
def postsingleGame(js, civ):
    return __postJson("deploygame", js, civ)    

def clearWaitingList():
    url = __getRestURL() + "/clearwaitinglist"
    r = requests.post(url)
    # code 204, no contents, expected here
    __getText(r)

def resumeGame(gameid, civ):
    url = __getRestURL() + f"/resumegame?gameid={gameid}&civ={civ}"
    r = requests.get(url)
    return __getText(r)
