import unittest
from BlockRetrieval import *

class BlockRetrievalTest(unittest.TestCase):
    
    def setUp(self):
        self.blockRetrieval = BlockRetrieval(Garage(3,3,3))
        
        
    def testFindLocationOfCarZero(self):
        self.assertEqual([0,0,0],self.blockRetrieval.getIndexForCarNumber(0))
        