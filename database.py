import sqlalchemy as db
import traceback
import logging
from datetime import datetime
from sys import exc_info


class SQLiteDataBase:
    def __init__(self, database_file):
        self.engine = db.create_engine('sqlite://' + database_file)
        self.connection = self.engine.connect()

    def insert_data(self, db_table, dataframe):
        sql_query = db.insert(db_table)
        data_list = dataframe.to_dict('list')
        self.connection.execute(sql_query, data_list)

