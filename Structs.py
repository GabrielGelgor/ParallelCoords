from abc import ABC, abstractmethod

class entry:                                                                        #Entry Class, Allows for the creation of an entry type data structure.
    def __init__ (self,key,obj):
        self.ent = [key,obj]

    def getK(self):
        return(self.ent[0])

    def getV(self):
        return(self.ent[1])

    def getAll(self):
        return self.ent

class data:                                                                         #Data structure used to split CSV data sets into alphanumeric records and numerical records.
    def __init__ (self,cData,aData):
        self.cData = cData
        self.aData = aData

    def getC(self):
        return self.cData

    def getA(self):
        return self.aData

class line:                                                                         #Data structure that facilitates creation of lines
    def __init__(self,y1,y2):
        self.y1 = y1
        self.y2 = y2
        self.x1 = 0
        self.x2 = 1

    def getM(self):
        return (self.y2-self.y1)

    def getLine(self):
        return('p1:',self.x1,',',self.y1,'p2:',self.x2,',',self.y2,'\n')

class rank_method(ABC):                                                             #Abstract class that forces any new ranking implementations contain a ranking method.
    def __init__ (self):
        pass

    @abstractmethod
    def rank(self,permutation) -> [int]:
        pass