import unittest
from languages.cpp import CPP


class TestCPP(unittest.TestCase):
    def test___init__(self):
        """Test case for CPP.__init__"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                CPP().__init__(*test_set[i]), res_set[i]
            )
        

if __name__ == '__main__':
    unittest.main()