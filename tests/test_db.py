import unittest
import schemadoc
from unittest.mock import patch
import sqlalchemy
import os

class DBTestCase(unittest.TestCase):
    _db_engine = None

    @staticmethod
    def get_db_engine():
        if not DBTestCase._db_engine:
            DBTestCase._db_engine = sqlalchemy.create_engine('sqlite://')
            sql_file = os.path.join(os.path.dirname(__file__), 'test_db.sql')
            with open(sql_file, "rt") as f:
                sql_text = f.read()
                for statement in sql_text.split(';'):
                    DBTestCase._db_engine.execute(statement)
        return DBTestCase._db_engine

    def test_db_create(self):
        # Should execute without errors
        engine = DBTestCase.get_db_engine()
        meta = sqlalchemy.MetaData()
        meta.reflect(bind=engine)
        self.assertGreater(len(meta.tables), 1, "It is expected that more than one table reflected.")

