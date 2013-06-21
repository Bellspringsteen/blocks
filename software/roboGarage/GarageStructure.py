import numpy as np

class Garage:
    def __init__(self,xAxisWide,yAxisWide,zAxisWide):
        self.__blocks = np.zeros(shape=(xAxisWide,yAxisWide,zAxisWide))
        self.__numberOfBlocks = (xAxisWide*yAxisWide*zAxisWide) -1
        self.setupInitialPosition()
        
    def setupInitialPosition(self):
        carNumberIterator = 0
        for zIterator in range(0,self.__blocks.shape[2]):
            for yIterator in range(0,self.__blocks.shape[1]):
                for xIterator in range(0,self.__blocks.shape[0]):
                    self.__blocks[xIterator][yIterator][zIterator] = carNumberIterator
                    carNumberIterator += 1
        self.__blocks[self.__blocks.shape[0]][self.__blocks.shape[1]][self.__blocks.shape[2]] = -1

                    
    def returnIndexOfCarNumber(self,carNumber):
        tuple =  np.where(self.__blocks == carNumber)
        return [tuple[0][0],tuple[1][0],tuple[2][0]]
        