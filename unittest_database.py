import unittest
from sqlalchemy.exc import ArgumentError
from database import SQLiteDataBase


class UnitTestDatabase(unittest.TestCase):

    def test_class_SQLiteDataBase(self):
        # check database class with
        db = SQLiteDataBase('/database/sqlitedatabase.db')
        self.assertIsInstance(db, SQLiteDataBase, "A Instance of SQLiteDataBase is expected")

        with self.assertRaises(ArgumentError):
            fail = SQLiteDataBase('not_existing_file')


if __name__ == '__main__':
    unittest.main()
