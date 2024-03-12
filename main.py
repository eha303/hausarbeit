import sys
import getopt
import logging
from database import SQLiteDataBase
import datasets


def main(argv):
    """
    this program reads train, test and ideal data
    finds the best ideal functions for the functions in the train data
    checks the test data to assign it to the found ideal functions
    writes everything to database
    :param argv: command line options could be:
     -t <testdatafile> -r <traindatafile> -i <idealdatafile> -d <databasefile>
    :return: None
    """
    # the ideal functions found are stored here:
    ideal_functions_found = []
    # configure logging
    logging.basicConfig(filename="error.log", filemode="a")
    # define data files if not overriden by command line option
    train_data_file = 'train.csv'
    test_data_file = 'test.csv'
    ideal_data_file = 'ideal.csv'
    # define database file if not overriden by command line option
    database_file = '/database/sqlitedatabase.db'
    # check command line options for alternative database and data files
    try:
        opts, args = getopt.getopt(argv, "ht:r:i:d:",
                                   ["testdata=", "traindata=", "idealdata=",
                                    "database="])
    except getopt.GetoptError:
        print('main.py -t <testdatafile> -r <traindatafile> -i <idealdatafile> -d <databasefile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -t <testdatafile> -r <traindatafile> -i <idealdatafile> -d <databasefile>')
            sys.exit()
        elif opt in ("-t", "--testdata"):
            test_data_file = arg
        elif opt in ("-r", "--traindata"):
            train_data_file = arg
        elif opt in ("-i", "--idealdata"):
            ideal_data_file = arg
        elif opt in ("-d", "--database"):
            database_file = arg
    # initialize sqlite database
    db = SQLiteDataBase(database_file)
    # create datasets
    test_data_set = datasets.TestDataSet('TestData', test_data_file)
    ideal_data_set = datasets.IdealDataSet('IdealData', ideal_data_file)
    train_data_set = datasets.DataSet('TrainData', train_data_file)
    # write ideal dataset to database
    ideal_db_success = ideal_data_set.write_to_database(db.engine)
    if ideal_db_success:
        print("Ideal Data stored in Database.")
    else:
        print("ERROR: Ideal Data NOT stored in Database. See error.log for more details.")
    # write train dataset to database
    train_db_success = train_data_set.write_to_database(db.engine)
    if train_db_success:
        print("Train Data stored in Database.")
    else:
        print("ERROR: Train Data NOT stored in Database. See error.log for more details.")
    train_dataframe = train_data_set.get_dataframe()

    train_data_columns = list(train_dataframe.columns.values)
    for c in train_data_columns:
        if c != 'x':
            print('Train Data checking column: ' + c)
            y_column = train_dataframe[c].tolist()
            result = ideal_data_set.compare_function(y_column)
            ideal_function_found = result['ideal_function_found']
            max_distance = result['max_distance']
            print('Ideal Function for ' + c + ' seems to be ' + ideal_function_found
                  + ' with the maximum distance ', max_distance)
            ideal_functions_found.append({"TrainFunction": c,
                                          "IdealFunction": ideal_function_found,
                                          "MaxDistance": max_distance})
    for ideal_function in ideal_functions_found:
        name_of_ideal_function = ideal_function['IdealFunction']
        max_distance = ideal_function['MaxDistance']
        test_data_set.check_coordinates_against_function(ideal_data_set.get_ideal_function_by_name(
            name_of_ideal_function), name_of_ideal_function, max_distance)
    # y_column = train_dataframe['y1'].tolist()
    # ideal_data_set.visualize_comparing_functions('y36', y_column, 'TrainData y1')


if __name__ == "__main__":
    main(sys.argv[1:])
