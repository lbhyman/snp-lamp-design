import unittest
import sys
sys.path.append('../')
import thermo_utils as tu

class TestThermoUtils(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_get_activation_new(self):
        sequences = {'non_mut_target' : 'TAAACAATCTATACAGGTAATTATAATTACCACCAACCTT',
                     'mut_target' : 'TAAACAATCTAAACAGGTAATTATAATTACCACCAACCTT',
                     'probeF' : 'AAGGTTGGTGGTAATTATAATTACCTGTTTAGATTGTTTA',
                     'probeQ' : 'TAAACAATCTAAACAGGTAATTATAATTACCACCAACCTT',
                     'sink' : 'AAGGTTGGTGGTAATTATAATTACCTGTATAGATTGTTTA',
                     'sinkC' : 'TAAACAATCTATACAGGTAATTATAATTACCACCAACCTT'}
        
        concentrations = {'non_mut_target' : 1e-7,
                     'mut_target': 1e-7,
                     'probeF' : 1e-7,
                     'probeQ' : 1e-7,
                     'sink' : 1e-7,
                     'sinkC' : 1e-7}
        
        params = {'temperature':21, 'sodium':0.065, 'magnesium':0.008}
        result = tu.get_activation_new(sequences, concentrations, params)
        keys = list(result.tubes.keys())[0]
        print(result['initial_state'].ensemble_pair_fractions)
        
if __name__ == '__main__':
    unittest.main()