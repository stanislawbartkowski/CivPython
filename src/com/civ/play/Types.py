from typing import Dict
import json


class CivO:

    _d: Dict

    def __init__(self, d: Dict):
        self._d = d

    def dumpj(self) -> str:
        return json.dumps(self._d)


class Point(CivO):

    def __init__(self, d: Dict):
        super().__init__(d)
        
    @classmethod        
    def initp(cls,row,col) :
        return cls({"row" : row, "col" : col})        

    @property
    def row(self) -> int:
        return self._d['row']

    @property
    def col(self) -> int:
        return self._d['col']
    
    def __eq__(self,other: any) -> bool :
        if type(other) == dict :
            return self.row == other['row'] and self.col == other['col']
        return self.row == other.row and self.col == other.col

class Figures(CivO):

    def __init__(self, d: Dict):
        super().__init__(d)
