import unittest
from graph_feature.main import generate_feature_file  # Example import

class TestGraphFeatures(unittest.TestCase):
    def test_generate_feature_file(self):
        result = generate_feature_file("../Resources/instances")
        self.assertEqual(result, 0)  # Example: check if function returns expected output

if __name__ == "__main__":
    unittest.main()
