import logging
import traceback
from datetime import datetime


class DataSet:
    def __init__(self, name, dataframe):
        self.name = name
        self.dataframe = dataframe
        self.number_of_columns = 4


class DataSetWithDatabaseFunctions(DataSet):
    def __init__(self, name, dataframe):
        DataSet.__init__(self, name, dataframe)
        self.database_success = True

    def write_to_database(self, engine):
        try:
            self.dataframe.to_sql(self.name, engine)

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
            database_success = False

        finally:
            return self.database_success
