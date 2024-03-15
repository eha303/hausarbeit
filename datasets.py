import logging
import math
import traceback
from datetime import datetime
import pandas
from matplotlib import pyplot as plt
from matplotlib import style
import pandas as pd
from sys import exc_info
from exceptions import InvalidDataFileError, InvalidFunctionDataError, InvalidDataFrameError


# this function does not need to be a class-method as it is static
def load_data_from_file(filename):
    """
    static function that loads data from a file, generates a dataframe and returns it
    :param filename: the filename with the data to load
    :return: dataframe with the data loaded from the file
    """
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
        logger.error("The following file was not found: %s", filename)
        # raise the exception again to make clear, no data was loaded
        raise FileNotFoundError


class DataSet:
    """
    This Class contains the dataframe with the function data
    and methods to compare this function data against other
    data, visualize functions and store data to database
    """

    def __init__(self, name, filename):
        """
        expects the name of the dataset and the filename with the data to load
        :param name: name of the dataset
        :param filename: name of the file that contains the data that should be loaded
        """
        self.database_success = True
        self.name = name
        self.filename = filename
        self.dataframe = load_data_from_file(filename)
        # check if something went wrong.
        # if data file could not been found, print a notice about that.
        # exception already thrown in static method load_data_from_file
        if not isinstance(self.dataframe, pandas.DataFrame):
            print('CRITICAL ERROR:')
            print(filename + ' not found. No Data has been loaded.')
            print('See error.log for more details about that.')
        # if data could not been loaded correctly from file because no correct
        # data was in the specified file, raise an other exception.
        try:
            if len(self.dataframe.columns) < 2:
                print('ERROR:')
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
        """
        renders a plot of the function
        :param y: name of the function in the dataframe [e.g. 'y1'] that should be visualized
        :return: None
        """
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
        """
        returns the dataframe containing the functions
        :return: the dataframe
        """
        return self.dataframe

    def compare_function(self, y_values):
        """
        compares the function submitted in parameter y_values against all functions
        in the dataframe, calculate the distance between the points, square this and sum
        all squared distances. the function that has the smallest value is recognized as
        the probably best fitting one and the name of the function will be returned
        together with the distance of the point that had the maximum distance from
        a point from the function in parameter y_values
        :param y_values: the function in y_values in a simple list that should be
         compared to any other function in this dataframe
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
            # which value-range is identical to the submitted list of y_values
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
                    # c is now the column-name of the function to be checked
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
                        # set the least_squared_distance to the actual
                        # sum_of_squared_distances and set the so far
                        # best fitting function to the actual checked one
                        # which name is stored in c
                        least_squared_distance = sum_of_squared_distances
                        ideal_function_found = c
                        max_distance = temp_max_distance
                    else:
                        # if the least squared distance is actually greater than
                        # the actual sum of least squared distances, set the actual
                        # found function with the least squared distance as new best
                        # fitting values
                        if least_squared_distance > sum_of_squared_distances:
                            least_squared_distance = sum_of_squared_distances
                            ideal_function_found = c
                            max_distance = temp_max_distance

            return_value = {"ideal_function_found": ideal_function_found, "max_distance": max_distance}
            return return_value

    def write_to_database(self, engine):
        """
        writes the dataframe to database
        and returns True if writing to database was successful
        or False when something went wrong
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
    """
    Enhances the class DataSet by a method called
    visualize_comparing_functions so that two functions
    could be rendered in one plot. This is useful for
    the IdealData to compare real data against it.
    This is also why this class is called IdealDataSet
    """

    def __init__(self, name, filename):
        """
        expects the name of the dataset and the filename with the data to load
        :param name: name of the dataset
        :param filename: name of the file that contains the data that should be loaded
        """
        DataSet.__init__(self, name, filename)

    def get_ideal_function_by_name(self, name):
        """
        returns a dataframe with the specified function
        :param name: name of the function that should be returned in a dataframe
        :return: the dataframe with the specified name
        """
        data = {'x': self.dataframe['x'].tolist(), 'y': self.dataframe[name].tolist()}
        return pd.DataFrame(data)

    def visualize_comparing_functions(self, y_function, y_values, name_of_comparing_function):
        """
        this method expects the name of an ideal function the object has in its dataframe
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
            ax.plot(x_list, y_list, label='Ideal Function ' + y_function, linewidth=2)
            ax.plot(x_list, y_values, label='Train Function ' + name_of_comparing_function, linewidth=1)
            ax.legend()
            ax.grid(True, color="k")
            plt.title('Ideal Function ' + y_function + ' and Train Function ' + name_of_comparing_function)
            plt.show()


class TestDataSet(DataSet):
    """
    Enhances the class DataSet by a method called
    check_coordinates_against_function which checks
    the coordinates in the dataframe against a function
    This is useful for the TestData to compare ideal data against it.
    This is also why this class is called TestDataSet
    """

    def __init__(self, name, filename):
        """
        expects the name of the dataset and the filename with the data to load
        adds column DeltaY and IdealFunction to the dataframe and fills it with
        0 and not_assigned
        :param name: name of the dataset
        :param filename: name of the file that contains the data that should be loaded
        """
        DataSet.__init__(self, name, filename)
        self.dataframe['DeltaY'] = [0] * self.dataframe.shape[0]
        self.dataframe['IdealFunction'] = ['not_assigned'] * self.dataframe.shape[0]

    def check_coordinates_against_function(self, function, name, max_distance):
        """
        checks every coordinate in the testdata against the
        function. if it is not more far away as the maximum
        distance multiplied by sqrt(2), the coordinate should
        be marked as a coordinate of the function.
        :param function: dataframe with the function
        :param name: name of the function
        :param max_distance: the maximum distance that should not be exceeded
        by the multiplication of sqrt(2)
        :return: None
        """
        # check if submitted function is a dataframe
        try:
            if not isinstance(function, pandas.DataFrame):
                raise InvalidDataFrameError

        except InvalidDataFrameError:
            now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
            exception_type, exception_value, exception_traceback = exc_info()
            file_name, line_number, procedure_name, line_code \
                = traceback.extract_tb(exception_traceback)[-1]
            # get Logging-Instance from Main Scope
            logger = logging.getLogger('__main__')
            logger.error("Exception Datetime: %s", now)
            logger.error("Exception Type: %s", exception_type)
            logger.error("Exception Value: %s", exception_value)
            logger.error("Message Value: %s", InvalidDataFrameError().error_message)
            logger.error("File Name: %s", file_name)
            logger.error("Line Number: %d", line_number)
            logger.error("Procedure Name: %s", procedure_name)
            logger.error("Line Code: %s", line_code)

        else:
            # calculate the maximum allowed distance between the points to be a
            # match by multiplying the maximum distance by the sqrt of two
            max_distance_mbsqrt2 = abs(max_distance) * math.sqrt(2)
            for i in self.dataframe.index:
                test_x = self.dataframe.loc[i, 'x']
                test_y = self.dataframe.loc[i, 'y']
                # finding the matching point by comparing only coordinates
                # which have the same x-value ist not correct.
                # a point could also be close to an ideal function with a
                # different x-value. so all coordinates from the ideal
                # function must be compared. so we have to iterate through
                # all the points from the ideal function and compare it
                # with the math.dist()-function against every coordinate
                # from the test data.
                for index in function.index:
                    ideal_x = function['x'][index]
                    ideal_y = function['y'][index]
                    # calculate distance between the coordinates
                    distance = math.dist([test_x, test_y], [ideal_x, ideal_y])
                    # if the distance between the two points is not greater
                    # than the maximum distance multiplied by sqrt(2), the
                    # point should be assigned to be on the ideal function
                    if abs(distance) <= max_distance_mbsqrt2:
                        # check if coordinate is not yet assigned to an ideal function
                        if self.dataframe.loc[i, 'IdealFunction'] == 'not_assigned':
                            # assign it and store the distance
                            self.dataframe.loc[i, 'IdealFunction'] = name
                            self.dataframe.loc[i, 'DeltaY'] = abs(distance)
                        # coordinate is already assigned to an ideal function
                        else:
                            # check if distance of the already assigned function
                            # is greater. if so, assign the actual checked coordinate
                            # to the actual function. if distance is smaller, leave
                            # it assigned to the already assigned ideal function
                            if self.dataframe.loc[i, 'DeltaY'] > distance:
                                # assign it and store the distance
                                self.dataframe.loc[i, 'IdealFunction'] = name
                                self.dataframe.loc[i, 'DeltaY'] = abs(distance)

    def visualize_test_data_with_ideal_function(self, idealfunction, name_of_ideal_function):
        """
        this method visualizes the test data coordinates with its assigned
        ideal function
        :param: idealfunction: the dataframe with the ideal function
        :param: name_of_ideal_function: the name of the ideal function
        :return: None
        """
        # check if submitted function is a dataframe
        try:
            if not isinstance(idealfunction, pandas.DataFrame):
                raise InvalidDataFrameError

        except InvalidDataFrameError:
            now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
            exception_type, exception_value, exception_traceback = exc_info()
            file_name, line_number, procedure_name, line_code \
                = traceback.extract_tb(exception_traceback)[-1]
            # get Logging-Instance from Main Scope
            logger = logging.getLogger('__main__')
            logger.error("Exception Datetime: %s", now)
            logger.error("Exception Type: %s", exception_type)
            logger.error("Exception Value: %s", exception_value)
            logger.error("Message Value: %s", InvalidDataFrameError().error_message)
            logger.error("File Name: %s", file_name)
            logger.error("Line Number: %d", line_number)
            logger.error("Procedure Name: %s", procedure_name)
            logger.error("Line Code: %s", line_code)

        else:
            x_list = idealfunction['x'].tolist()
            y_list = idealfunction['y'].tolist()
            # get all testdata coordinates assigned to the ideal function
            test_data_x_list = []
            test_data_y_list = []
            for i in self.dataframe.index:
                if self.dataframe.loc[i, 'IdealFunction'] == name_of_ideal_function:
                    test_data_x_list.append(self.dataframe.loc[i, 'x'])
                    test_data_y_list.append(self.dataframe.loc[i, 'y'])
            # render it
            style.use('ggplot')
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_list, y_list, label='Ideal Function ' + name_of_ideal_function, linewidth=2)
            ax.plot(test_data_x_list, test_data_y_list, 'bo', label='Test Data')
            ax.legend()
            ax.grid(True, color="k")
            plt.title('Test Data assigned to Ideal Function ' + name_of_ideal_function)
            plt.show()

    def visualize_test_data_without_assignment(self):
        """
        this method visualizes the test data coordinates
        that could not be assigned to an ideal function
        :return: None
        """
        # get all testdata coordinates with no assignment
        test_data_x_list = []
        test_data_y_list = []
        for i in self.dataframe.index:
            if self.dataframe.loc[i, 'IdealFunction'] == 'not_assigned':
                test_data_x_list.append(self.dataframe.loc[i, 'x'])
                test_data_y_list.append(self.dataframe.loc[i, 'y'])
        # render it
        style.use('ggplot')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(test_data_x_list, test_data_y_list, 'bo', label='Test Data')
        ax.legend()
        ax.grid(True, color="k")
        plt.title('Test Data with no assignment to an Ideal Function')
        plt.show()
