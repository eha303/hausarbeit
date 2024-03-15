import sqlalchemy as db
import logging
import traceback
from datetime import datetime
from sys import exc_info
from sqlalchemy.exc import ArgumentError


class SQLiteDataBase:
    """
    Initializes a SQLite Database Connection and Engine
    with the given Database File
    """

    def __init__(self, database_file):
        """
        Initializes a SQLite Database Connection and Engine
        with the given Database File
        :param database_file: the SQLite Database File (could include a Path)
        """
        try:
            self.engine = db.create_engine('sqlite://' + database_file)
            self.connection = self.engine.connect()

        except ArgumentError:
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
            raise ArgumentError

    def insert_data(self, db_table, dataframe):
        """
        Writes a complete Table to Database
        :param db_table: the Database Table Name that should be created
        :param dataframe: the Data for the Table as a Dataframe
        :return:
        """
        sql_query = db.insert(db_table)
        data_list = dataframe.to_dict('list')
        self.connection.execute(sql_query, data_list)
