from GarageStructure import Garage
import numpy as np

class BlockRetrieval:
    
    def __init__(self,garage):
        self.garage = garage
        
    def getIndexForCarNumber(self,carNumber):
        return self.garage.returnIndexOfCarNumber(carNumber)