import unittest
from languages.c import C


class TestC(unittest.TestCase):
    def test___init__(self):
        """Test case for C.__init__"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                C().__init__(*test_set[i]), res_set[i]
            )
        

if __name__ == '__main__':
    unittest.main()