import math
import sys
import getopt
import logging
from database import SQLiteDataBase
import datasets


def handle_exception(errormessage):
    """
    Handles critical exceptions and let the user decide
    if the program should be interrupted or continued
    :param errormessage: the errormessage from the exception that appeared
    :return: None
    """
    print('ERROR:')
    print(errormessage)
    print('Please see error.log for more details.')
    print('The program probably will not run correctly.')
    print('Do you want to continue anyway?')
    print('[Y] - Yes, continue anyway.')
    print('[Q] - No, quit the program.')
    user_input = ''
    while user_input.upper() != 'Y':
        user_input = input('Please enter Y or Q: ')
        if user_input.upper() == 'Q':
            sys.exit(0)


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
    # the data is stored in datasets which are declared here already
    # and initialized with None, because they are initialized later
    # on in a try-except-block, so it is unclear for the linter that
    # they are really initialized so it shows an error.
    ideal_data_set = None
    train_data_set = None
    test_data_set = None
    # same thing with the deal functions:
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
    options_set = False
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -t <testdatafile> -r <traindatafile> -i <idealdatafile> -d <databasefile>')
            sys.exit()
        elif opt in ("-t", "--testdata"):
            test_data_file = arg
            options_set = True
        elif opt in ("-r", "--traindata"):
            train_data_file = arg
            options_set = True
        elif opt in ("-i", "--idealdata"):
            ideal_data_file = arg
            options_set = True
        elif opt in ("-d", "--database"):
            database_file = arg
            options_set = True
    print('\nUsage: main.py -t <testdatafile> -r <traindatafile> -i <idealdatafile> -d <databasefile>\n')
    if not options_set:
        print('No options set. Using preset options for data files:')
    print('Testdata File: ' + test_data_file)
    print('Traindata File: ' + train_data_file)
    print('Idealdata File: ' + ideal_data_file)
    print('SQLite Database File: ' + database_file)
    input('\nPress Enter to start reading Data Files an initialize Database.')

    # initialize sqlite database
    db = SQLiteDataBase(database_file)
    if isinstance(db, SQLiteDataBase):
        print('Database initialized successfully.')
    else:
        print('ERROR: Database could not be initialized. See error.log for more Details.')
    # create datasets
    try:
        test_data_set = datasets.TestDataSet('TestData', test_data_file)
    except FileNotFoundError:
        handle_exception(test_data_file + " could not been found.")
    try:
        ideal_data_set = datasets.IdealDataSet('IdealData', ideal_data_file)
    except FileNotFoundError:
        handle_exception(ideal_data_file + " could not been found.")
    try:
        train_data_set = datasets.DataSet('TrainData', train_data_file)
    except FileNotFoundError:
        handle_exception(train_data_file + " could not been found.")
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
    # now find the best fitting ideal data functions for
    # every function in the train data set
    train_data_columns = list(train_dataframe.columns.values)
    print('Starting to calculate the best fitting ideal data function for every function in the train data set...')
    for c in train_data_columns:
        if c != 'x':
            print('Train data checking function: ' + c)
            y_column = train_dataframe[c].tolist()
            result = ideal_data_set.compare_function(y_column)
            ideal_function_found = result['ideal_function_found']
            max_distance = result['max_distance']
            print('Best fitting ideal function for train data function ' + c + ' is ' + ideal_function_found)
            print('with the maximum distance between two points of ', max_distance)
            ideal_functions_found.append({"TrainFunction": c,
                                          "IdealFunction": ideal_function_found,
                                          "MaxDistance": max_distance})
    # now check every coordinate in the Test Data and assign it
    # to a found ideal function if the test data coordinate is not
    # more far away than sqrt(2) * max_distance of the point most far
    # away from the train data
    print('Start checking every coordinate in the Test Data against the found ideal functions.')
    for ideal_function in ideal_functions_found:
        name_of_ideal_function = ideal_function['IdealFunction']
        max_distance = ideal_function['MaxDistance']
        print('\nComparing every coordinate in Test Data against Ideal Function ' + name_of_ideal_function)
        print('with the Maximum Distance from the Train Data of', max_distance)
        print('which will result in the criteria of', max_distance, '* sqrt(2) =', max_distance*math.sqrt(2))
        print('Every point which is not more far away from the ideal function will be assigned to it.')
        test_data_set.check_coordinates_against_function(ideal_data_set.get_ideal_function_by_name(
            name_of_ideal_function), name_of_ideal_function, max_distance)
    test_db_success = test_data_set.write_to_database(db.engine)
    if test_db_success:
        print("\nTest Data stored in Database.")
    else:
        print("\nERROR: Test Data NOT stored in Database. See error.log for more details.")
    # everything is calculated and written to database
    # show the command line menu
    user_input = ''
    while user_input.upper() != 'Q':
        print('\n')
        print('[1] - Visualize the found ideal functions')
        print('[2] - Visualize the found ideal functions in comparison to the train function')
        print('[3] - Visualize assigned and not assigned test data')
        print('[4] - Visualize all ideal functions')
        print('[Q] - Quit')
        user_input = input('Please enter [1-4] or Q to Quit: ')
        if user_input == '1':
            print('\n')
            while user_input.upper() != 'B':
                n = 0
                for ideal_function in ideal_functions_found:
                    n += 1
                    print('[' + str(n) + '] - Visualize the found ideal function ' + ideal_function['IdealFunction'])
                print('[B] - go Back to main menu')
                user_input = input('Please enter [1-' + str(n) + '] or B for Back: ')
                n = 1
                for ideal_function in ideal_functions_found:
                    if str(n) == user_input:
                        ideal_data_set.visualize_function(ideal_function['IdealFunction'])
                    n += 1
        elif user_input == '2':
            print('\n')
            while user_input.upper() != 'B':
                n = 0
                for ideal_function in ideal_functions_found:
                    n += 1
                    print('[' + str(n) + '] - Visualize ideal function ' + ideal_function['IdealFunction'] +
                          ' and train function ' + ideal_function['TrainFunction'])
                print('[B] - go Back to main menu')
                user_input = input('Please enter [1-' + str(n) + '] or B for Back: ')
                n = 1
                for ideal_function in ideal_functions_found:
                    if str(n) == user_input:
                        y_values = train_data_set.get_dataframe()[ideal_function['TrainFunction']].tolist()
                        ideal_data_set.visualize_comparing_functions(ideal_function['IdealFunction'], y_values,
                                                                     ideal_function['TrainFunction'])
                    n += 1
        elif user_input == '3':
            print('\n')
            while user_input.upper() != 'B':
                n = 0
                for ideal_function in ideal_functions_found:
                    n += 1
                    print('[' + str(n) + '] - Visualize ideal function ' + ideal_function['IdealFunction'] +
                          ' and assigned Test Data')
                print('[N] - Visualize not assigned Test Data which did not match the criteria')
                print('[B] - go Back to main menu')
                user_input = input('Please enter [1-' + str(n) + '] or N or B for Back: ')
                n = 1
                for ideal_function in ideal_functions_found:
                    if str(n) == user_input:
                        ideal_function_df = ideal_data_set.get_ideal_function_by_name(ideal_function['IdealFunction'])
                        test_data_set.visualize_test_data_with_ideal_function(ideal_function_df,
                                                                              ideal_function['IdealFunction'])
                    n += 1
                if user_input.upper() == 'N':
                    test_data_set.visualize_test_data_without_assignment()
        elif user_input == '4':
            print('\n')
            while user_input.upper() != 'B':
                number_of_ideal_functions = len(ideal_data_set.get_dataframe().columns)
                # decrease number_of_ideal_functions by 1 because first column in the
                # dataframe is the x-axis
                number_of_ideal_functions -= 1
                print('There are ' + str(number_of_ideal_functions) + ' ideal functions.')
                user_input = input('Please enter [1-' + str(number_of_ideal_functions) + '] or B for Back: ')
                if user_input.upper() != 'B':
                    try:
                        input_value = int(user_input)
                        if (input_value <= number_of_ideal_functions) & (input_value > 0):
                            ideal_function_name = 'y' + str(input_value)
                            ideal_data_set.visualize_function(ideal_function_name)
                        else:
                            print('Invalid Input. Please enter a number between 1 and ' +
                                  str(number_of_ideal_functions))
                    except ValueError:
                        print('Invalid Input. Please enter a number between 1 and ' + str(number_of_ideal_functions))

        elif user_input.upper() == 'Q':
            sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
