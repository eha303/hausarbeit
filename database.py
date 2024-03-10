import sqlalchemy as db
import traceback
import logging
from datetime import datetime
from sys import exc_info


class DataBase:
    def __init__(self):
        self.engine = db.create_engine('sqlite:///database/sqlitedatabase.db')
        self.connection = self.engine.connect()

    def insert_data(self, db_table, dataframe):
        sql_query = db.insert(db_table)
        data_list = dataframe.to_dict('list')
        self.connection.execute(sql_query, data_list)

    def create_table_from_dataframe(self, table_name, dataframe):
        success = True

        try:
            dataframe.to_sql(table_name, self.engine)

        except ValueError:
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
            success = False

        finally:
            return success