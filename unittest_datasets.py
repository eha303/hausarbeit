import unittest
import pandas
import datasets as ds
from exceptions import InvalidFunctionDataError, InvalidDataFileError


class UnitTestDatasetOperations(unittest.TestCase):
    def test_load_data_from_file(self):
        # check data file loading
        result = ds.load_data_from_file('test.csv')
        self.assertIsInstance(result, pandas.DataFrame, "A DataFrame should be returned")

        # check data file loading with not existing file
        # FileNotFoundError should be raised
        with self.assertRaises(FileNotFoundError):
            ds.load_data_from_file('not_exisiting_file')

    def test_class_DataSet(self):
        # check class dataset
        data_set = ds.DataSet('DataSet', 'train.csv')
        self.assertIsInstance(data_set, ds.DataSet)

        # check class instantiation with not existing data file
        with self.assertRaises(FileNotFoundError):
            ds.DataSet('This should raise an exception', 'not_exisiting_file')

        # check class instantiation with invalid data file
        with self.assertRaises(InvalidDataFileError):
            ds.DataSet('This should raise an Invalid Data File Exception', 'error.csv')

        # dataframe should be returned
        dataframe = data_set.get_dataframe()
        self.assertIsInstance(dataframe, pandas.DataFrame)

        # list of y-coordinates will be taken from a train-function-dataset itself
        # so it is the same and should be identified for sure
        y_column = dataframe['y1'].tolist()
        result = data_set.compare_function(y_column)

        # result is a dictionary with the name of the ideal function
        # and the maximum distance. as a function taken from the dataset
        # itself was submitted for comparing, the name of the submitted
        # function should be the same and the maximum distance should be 0
        expected_result = {"ideal_function_found": 'y1', "max_distance": 0}
        self.assertDictEqual(result, expected_result)

        # when invalid data is submitted to compare_function an InvalidFunctionDataError
        # should be raised
        with self.assertRaises(InvalidFunctionDataError):
            data_set.compare_function('this is invalid data')

        # writing to database could not be tested without an instance
        # of a test-database which is not present. so only testing
        # if writing to database fails because of an invalid database engine
        # object results in expected return value of False
        # the exceptions raised are catched in function itself and logged
        # to error.log because failing with writing data to database is not
        # a critical error. the program itself should run without the fact
        # that data is written correctly to database
        return_value = data_set.write_to_database(None)
        self.assertFalse(return_value, 'Excpected to be False as no database engine is present')

    def test_class_IdealDataSet(self):
        # check class IdealDataSet
        ideal_data_set = ds.IdealDataSet('IdealDataSet', 'ideal.csv')
        self.assertIsInstance(ideal_data_set, ds.IdealDataSet)

        # check class instantiation with not existing data file
        with self.assertRaises(FileNotFoundError):
            ds.IdealDataSet('This should raise an exception', 'not_exisiting_file')

        # check class instantiation with invalid data file
        with self.assertRaises(InvalidDataFileError):
            ds.IdealDataSet('This should raise an Invalid Data File Exception', 'error.csv')

        # should return a dataframe with the selected function
        result = ideal_data_set.get_ideal_function_by_name('y1')
        self.assertIsInstance(result, pandas.DataFrame)

    def test_class_TestDataSet(self):
        # check class TestDataSet
        test_data_set = ds.TestDataSet('TestDataSet', 'test.csv')
        self.assertIsInstance(test_data_set, ds.TestDataSet)

        # check class instantiation with not existing data file
        with self.assertRaises(FileNotFoundError):
            ds.TestDataSet('This should raise an File Not Found Exception', 'not_exisiting_file')

        # check class instantiation with invalid data file
        with self.assertRaises(InvalidDataFileError):
            ds.TestDataSet('This should raise an Invalid Data File Exception', 'error.csv')


if __name__ == '__main__':
    unittest.main()
