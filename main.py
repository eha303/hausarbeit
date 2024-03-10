import os
import traceback
import logging
from datetime import datetime
from sys import exc_info
import pandas as pd
from database import DataBase
from data import DataSet


def load_data_from_file(filename):
    try:
        # try to load data into dataframe and return it
        dat: pd.DataFrame = pd.read_csv(filename)
        return dat

    except FileNotFoundError:
        now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        exception_type, exception_value, exception_traceback = exc_info()
        file_name, line_number, procedure_name, line_code \
            = traceback.extract_tb(exception_traceback)[-1]
        # get Logging-Instance from Main Scope
        logger = logging.getLogger('__main__')
        logger.error("Exception Datetime: %s", now)
        logger.error("Exception Type: %s", exception_type)
        logger.error("Exception Value: %s", exception_value)
        logger.error("File Name: %s", file_name)
        logger.error("Line Number: %d", line_number)
        logger.error("Procedure Name: %s", procedure_name)
        logger.error("Line Code: %s", line_code)
        # return None to make clear no data has been loaded
        return None


if __name__ == '__main__':
    my_db = DataBase()

    # configure logging
    logging.basicConfig(filename="error.log", filemode="a")

    test_data = load_data_from_file('test.csv')
    if test_data is None:
        print("Testdata not loaded. File test.csv not found.")
    else:
        # create new object from class DataSet
        test_data_set = DataSet('TestData', test_data)
        # set the correct number of columns for this dataframe
        test_data_set.number_of_columns = len(test_data.columns)
        print("Testdata loaded.")
    ideal_data = load_data_from_file('ideal.csv')
    if ideal_data is None:
        print("Ideal Data not loaded. File ideal.csv not found.")
    else:
        # create new object from class DataSet
        ideal_data_set = DataSet('IdealData', ideal_data)
        # set the correct number of columns for this dataframe
        ideal_data_set.number_of_columns = len(ideal_data.columns)
        print("Ideal Data loaded.")
    train_data = load_data_from_file('train.csv')
    if train_data is None:
        print("Train Data not loaded. File train.csv not found.")
    else:
        # create new object from class DataSet
        train_data_set = DataSet('TrainData', train_data)
        # set the correct number of columns for this dataframe
        train_data_set.number_of_columns = len(train_data.columns)
        print("Train Data loaded.")
    ideal_db_success = my_db.create_table_from_dataframe("ideal_data",
                                                         ideal_data)
    if ideal_db_success:
        print("Ideal Data stored in Database.")
    else:
        print("Ideal Data NOT stored in Database. Table already exists.\
        Probably you ran the program already and tables have been created.")
    train_db_success = my_db.create_table_from_dataframe("train_data",
                                                         train_data)
    if train_db_success:
        print("Train Data stored in Database.")
    else:
        print("Train Data NOT stored in Database. Table already exists.\
        Probably you ran the program already and tables have been created.")
