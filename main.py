import logging
from database import DataBase
from data import DataSetWithDatabaseFunctions


if __name__ == '__main__':
    my_db = DataBase()

    # configure logging
    logging.basicConfig(filename="error.log", filemode="a")
    test_data_set = DataSetWithDatabaseFunctions('TestData', 'test.csv')
    ideal_data_set = DataSetWithDatabaseFunctions('IdealData', 'ideal.csv')
    train_data_set = DataSetWithDatabaseFunctions('TrainData', 'train.csv')

    ideal_db_success = ideal_data_set.write_to_database(my_db.engine)
    if ideal_db_success:
        print("Ideal Data stored in Database.")
    else:
        print("Ideal Data NOT stored in Database. Table already exists.\
        Probably you ran the program already and tables have been created.")
    train_db_success = train_data_set.write_to_database(my_db.engine)
    if train_db_success:
        print("Train Data stored in Database.")
    else:
        print("Train Data NOT stored in Database. Table already exists.\
        Probably you ran the program already and tables have been created.")

    train_data_set.visualize_data('x', 'y4')
