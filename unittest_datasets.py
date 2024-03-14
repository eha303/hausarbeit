import unittest
import pandas

import datasets as ds


class UnitTestDatasetOperations(unittest.TestCase):
    def test_load_data_from_file(self):
        """
        check data file loading
        """
        result = ds.load_data_from_file('test.csv')
        self.assertIsInstance(result, pandas.DataFrame, "A DataFrame should be returned")
        result = ds.load_data_from_file('not_exisiting_file')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
