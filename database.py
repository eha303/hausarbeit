import sqlalchemy as db

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
        self.engine = db.create_engine('sqlite://' + database_file)
        self.connection = self.engine.connect()

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

