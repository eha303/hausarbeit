import sys
import getopt
import logging
from database import SQLiteDataBase
from data import DataSet
from data import IdealDataSet


def main(argv):
    # start
    # configure logging
    logging.basicConfig(filename="error.log", filemode="a")
    # define data files
    train_data_file = 'train.csv'
    test_data_file = 'test.csv'
    ideal_data_file = 'ideal.csv'
    # define database file
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
    my_db = SQLiteDataBase(database_file)
    # create datasets
    test_data_set = DataSet('TestData', test_data_file)
    ideal_data_set = IdealDataSet('IdealData', ideal_data_file)
    train_data_set = DataSet('TrainData', train_data_file)
    # write ideal dataset to database
    ideal_db_success = ideal_data_set.write_to_database(my_db.engine)
    if ideal_db_success:
        print("Ideal Data stored in Database.")
    else:
        print("ERROR: Ideal Data NOT stored in Database. See error.log for more details.")
    # write train dataset to database
    train_db_success = train_data_set.write_to_database(my_db.engine)
    if train_db_success:
        print("Train Data stored in Database.")
    else:
        print("ERROR: Train Data NOT stored in Database. See error.log for more details.")
    # train_data_set.visualize_data('x', 'y4')
    train_dataframe = train_data_set.get_dataframe()
    x_column = train_dataframe['x'].tolist()
    train_data_columns = list(train_dataframe.columns.values)
    for c in train_data_columns:
        if c != 'x':
            print('train data checking column: ' + c)
            y_column = train_dataframe[c].tolist()
            result = ideal_data_set.compare_function(y_column)
            print('Ideal Function for ' + c + ' seems to be ' + result["ideal_function_found"]
                  + ' with the maximum distance ', result['max_distance'])
    y_column = train_dataframe['y1'].tolist()
    ideal_data_set.visualize_comparing_functions('y36', y_column, 'TrainData y1')


if __name__ == "__main__":
    main(sys.argv[1:])
