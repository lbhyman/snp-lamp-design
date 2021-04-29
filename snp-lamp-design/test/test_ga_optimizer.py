import unittest
import sys
sys.path.append('../')
from ga_optimizer import GAOptimizer

class TestThermoUtils(unittest.TestCase):
    
    def setUp(self):
        self.optimizer = GAOptimizer()
        pass
        
    def tearDown(self):
        pass
    
    def test_predict_nupack_calls(self):
        self.assertEqual(305, self.optimizer.predict_nupack_calls(128))
        self.assertEqual(561, self.optimizer.predict_nupack_calls(256))
        self.assertEqual(8241, self.optimizer.predict_nupack_calls(4096))
        self.assertEqual(51, self.optimizer.predict_nupack_calls(1))
        self.assertEqual(50, self.optimizer.predict_nupack_calls(0))
        
if __name__ == '__main__':
    unittest.main()