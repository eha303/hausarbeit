import logging
import traceback
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import style
import pandas as pd
from sys import exc_info
from exceptions import InvalidDataFileError, InvalidFunctionDataError


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
        """
        compares the function submitted by the parameter y_values against all functions
        in the dataframe, calculate the distance between the points, square this and sum
        all squared distances. the function that has the smallest value is recognized as
        the probably best fitting one and the name of the function will be returned
        together with the distance of the point that had the maximum distance from
        a point from the function in parameter y_values
        :param y_values: the function that should be compared to any other function in this dataframe
        :return: A Dictionary with the ideal_function_found and the max_distance
        """
        # check if submitted y_values is a list of float values as expected
        try:
            invalid_function_data = False
            if not isinstance(y_values, list):
                invalid_function_data = True

            else:
                for i in y_values:
                    if not isinstance(i, float):
                        invalid_function_data = True

            if invalid_function_data:
                raise InvalidFunctionDataError

        except InvalidFunctionDataError:
            now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
            exception_type, exception_value, exception_traceback = exc_info()
            file_name, line_number, procedure_name, line_code \
                = traceback.extract_tb(exception_traceback)[-1]
            # get Logging-Instance from Main Scope
            logger = logging.getLogger('__main__')
            logger.error("Exception Datetime: %s", now)
            logger.error("Exception Type: %s", exception_type)
            logger.error("Exception Value: %s", exception_value)
            logger.error("Message Value: %s", InvalidFunctionDataError().error_message)
            logger.error("File Name: %s", file_name)
            logger.error("Line Number: %d", line_number)
            logger.error("Procedure Name: %s", procedure_name)
            logger.error("Line Code: %s", line_code)
            # return None to indicate something went wrong
            return None

        else:
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
            max_distance = 0
            for c in dataframe_columns:
                sum_of_squared_distances = 0
                temp_max_distance = 0
                if c != 'x':
                    #print('now checking ' + c)
                    y_column = self.dataframe[c].tolist()
                    i = 0
                    while i < len(y_column):
                        distance = y_column[i] - y_values[i]
                        if distance > temp_max_distance:
                            temp_max_distance = distance
                        squared_distance = distance * distance
                        sum_of_squared_distances += squared_distance
                        i += 1

                    if least_squared_distance == 0:
                        #print('_least squared distance is actually: ', least_squared_distance)
                        least_squared_distance = sum_of_squared_distances
                        ideal_function_found = c
                        max_distance = temp_max_distance
                        #print('sum of squared distance is: ', sum_of_squared_distances)
                        #print('ideal function found: ' + c)
                    else:
                        #print('least squared distance is actually: ', least_squared_distance)
                        #print('actual sum of least squared distance is: ', sum_of_squared_distances)
                        if least_squared_distance > sum_of_squared_distances:
                            least_squared_distance = sum_of_squared_distances
                            ideal_function_found = c
                            max_distance = temp_max_distance
                            #print('sum of squared distance is: ', sum_of_squared_distances)
                            #print('ideal function found: ' + c)
            return_value = {"ideal_function_found": ideal_function_found, "max_distance": max_distance}
            return return_value

    def write_to_database(self, engine):
        """
        writes the dataframe to database
        and returns True if writing to database was successful
        or False of something went wrong
        :param engine: the database-engine
        :return: Success
        """
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
        """
        this method expects the name of an ideal functions the objects has in its dataframe
        and another function that should be compared to the chosen ideal function.
        both functions will be visualized by rendering a matplotlib-plot
        :param y_function: the name of the ideal function in the own dataset that should be compared
        :param y_values: a list of y_values that describes the function that should be compared
                         against the selected ideal function chosen in parameter y_function
        :param name_of_comparing_function: the name of the function submitted with parameter y_values
        :return: None
        """
        # check if submitted y_values is a list of float values as expected
        try:
            invalid_function_data = False
            if not isinstance(y_values, list):
                invalid_function_data = True

            else:
                for i in y_values:
                    if not isinstance(i, float):
                        invalid_function_data = True

            if invalid_function_data:
                raise InvalidFunctionDataError

        except InvalidFunctionDataError:
            now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
            exception_type, exception_value, exception_traceback = exc_info()
            file_name, line_number, procedure_name, line_code \
                = traceback.extract_tb(exception_traceback)[-1]
            # get Logging-Instance from Main Scope
            logger = logging.getLogger('__main__')
            logger.error("Exception Datetime: %s", now)
            logger.error("Exception Type: %s", exception_type)
            logger.error("Exception Value: %s", exception_value)
            logger.error("Message Value: %s", InvalidFunctionDataError().error_message)
            logger.error("File Name: %s", file_name)
            logger.error("Line Number: %d", line_number)
            logger.error("Procedure Name: %s", procedure_name)
            logger.error("Line Code: %s", line_code)

        else:
            x_list = self.dataframe['x'].tolist()
            y_list = self.dataframe[y_function].tolist()
            style.use('ggplot')
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_list, y_list, label=self.name + ' ' + y_function, linewidth=2)
            ax.plot(x_list, y_values, label=name_of_comparing_function, linewidth=1)
            ax.legend()
            ax.grid(True, color="k")
            plt.title(self.name + ' ' + y_function + ' and ' + name_of_comparing_function)
            plt.show()
