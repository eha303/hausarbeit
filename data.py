import logging
import traceback
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import style
import pandas as pd
from sys import exc_info
from exceptions import InvalidDataFileError


# does not need to be a class-method as it is static
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


class DataSet:
    def __init__(self, name, filename):
        self.database_success = True
        self.name = name
        self.filename = filename
        self.dataframe = load_data_from_file(filename)
        # check if something went wrong.
        # if data file could not been found, print a notice about that.
        # exception already thrown in static method load_data_from_file
        if self.dataframe is None:
            print(filename + ' not found. No Data has been loaded.')
        # if data could not been loaded correctly from file because no correct
        # data was in the specified file, raise an other exception.
        try:
            if len(self.dataframe.columns) < 2:
                print(filename + ' does not seem to be a valid data file.')
                print('See error.log for more details about that.')
                raise InvalidDataFileError

        except InvalidDataFileError:
            now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
            exception_type, exception_value, exception_traceback = exc_info()
            file_name, line_number, procedure_name, line_code \
                = traceback.extract_tb(exception_traceback)[-1]
            # get Logging-Instance from Main Scope
            logger = logging.getLogger('__main__')
            logger.error("Exception Datetime: %s", now)
            logger.error("Exception Type: %s", exception_type)
            logger.error("Exception Value: %s", exception_value)
            logger.error("Message Value: %s", InvalidDataFileError().error_message)
            logger.error("File Name: %s", file_name)
            logger.error("Line Number: %d", line_number)
            logger.error("Procedure Name: %s", procedure_name)
            logger.error("Line Code: %s", line_code)

    def visualize_function(self, y):
        x_list = self.dataframe['x'].tolist()
        y_list = self.dataframe[y].tolist()
        style.use('ggplot')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_list, y_list, label=y, linewidth=2)
        ax.legend()
        ax.grid(True, color="k")
        plt.title(self.name + ' Function ' + y)
        plt.show()

    def get_dataframe(self):
        return self.dataframe

    def compare_function(self, y_values):
        ideal_function_found = None
        # get the column names of this dataframe
        dataframe_columns = list(self.dataframe.columns.values)
        # it is expected that every dataframe has a x-axis column named 'x'
        # which value-range is identical to the submitted y_values
        # iterate through every y-column in this dataframe
        # and compare it to the submitted y_values,
        # calculate the distance between the points, square this and sum all
        # squared distances. if the sum of the squared distances is smaller
        # than the previous one, store this function as the probably best
        # fitting one.
        least_squared_distance = 0
        for c in dataframe_columns:
            sum_of_squared_distances = 0
            if c != 'x':
                #print('now checking ' + c)
                y_column = self.dataframe[c].tolist()
                i = 0
                while i < len(y_column):
                    distance = y_column[i] - y_values[i]
                    squared_distance = distance * distance
                    sum_of_squared_distances += squared_distance
                    i += 1

                if least_squared_distance == 0:
                    #print('_least squared distance is actually: ', least_squared_distance)
                    least_squared_distance = sum_of_squared_distances
                    ideal_function_found = c
                    #print('sum of squared distance is: ', sum_of_squared_distances)
                    #print('ideal function found: ' + c)
                else:
                    #print('least squared distance is actually: ', least_squared_distance)
                    #print('actual sum of least squared distance is: ', sum_of_squared_distances)
                    if least_squared_distance > sum_of_squared_distances:
                        least_squared_distance = sum_of_squared_distances
                        ideal_function_found = c
                        #print('sum of squared distance is: ', sum_of_squared_distances)
                        #print('ideal function found: ' + c)
        return ideal_function_found

    def write_to_database(self, engine):
        try:
            self.dataframe.to_sql(self.name, engine, if_exists='replace')

        except ValueError:
            now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
            from sys import exc_info
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
            self.database_success = False

        finally:
            return self.database_success


class IdealDataSet(DataSet):
    def __init__(self, name, filename):
        DataSet.__init__(self, name, filename)

    def visualize_comparing_functions(self, y_function, y_values, name_of_comparing_function):
        x_list = self.dataframe['x'].tolist()
        y_list = self.dataframe[y_function].tolist()
        style.use('ggplot')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_list, y_list, label=self.name + ' ' + y_function, linewidth=2)
        ax.plot(x_list, y_values, label=name_of_comparing_function, linewidth=2)
        ax.legend()
        ax.grid(True, color="k")
        plt.title(self.name + y_function + ' and ' + name_of_comparing_function)
        plt.show()
