import unittest
from BlockRetrieval import *

class BlockRetrievalTest(unittest.TestCase):
    
    def setUp(self):
        self.blockRetrieval = BlockRetrieval(Garage(3,3,3))
        
        
    def testFindLocationOfCarZero(self):
        self.assertEqual([0,0,0],self.blockRetrieval.getIndexForCarNumber(0))
        
    def moveBlockOneToPositionTwo(self):
        self.blockRetrieval.move(1,3);
        self.assertEqual([2,0,0],self.blockRetrieval.getIndexForCarNumber(1))
        