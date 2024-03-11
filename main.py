import sys, getopt
import logging
from database import SQLiteDataBase
from data import DataSetWithDatabaseFunctions


def main(argv):
    # configure logging
    logging.basicConfig(filename="error.log", filemode="a")
    # define data files
    traindata_file = 'train.csv'
    testdata_file = 'test.csv'
    idealdata_file = 'ideal.csv'
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
            testdata_file = arg
        elif opt in ("-r", "--traindata"):
            traindata_file = arg
        elif opt in ("-i", "--idealdata"):
            idealdata_file = arg
        elif opt in ("-d", "--database"):
            database_file = arg
    # initialize sqlite database
    my_db = SQLiteDataBase(database_file)
    # create datasets
    error_data_set = DataSetWithDatabaseFunctions('ErrorData', 'error.txt')
    test_data_set = DataSetWithDatabaseFunctions('TestData', testdata_file)
    ideal_data_set = DataSetWithDatabaseFunctions('IdealData', idealdata_file)
    train_data_set = DataSetWithDatabaseFunctions('TrainData', traindata_file)
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


if __name__ == "__main__":
    main(sys.argv[1:])
