import unittest
import schemadoc
from unittest.mock import patch
import sqlalchemy
import os
import shutil

class DBTestCase(unittest.TestCase):

    def _get_output_folder(self):
        return os.path.join(os.path.dirname(__file__), 'test_output')


    def _delete_test_folder(self):
        p = self._get_output_folder()
        if os.path.exists(p):
            shutil.rmtree(p)

    def __init__(self, method_name):
        self._db_engine = None
        super(DBTestCase, self).__init__(method_name)

    def get_db_engine(self):
        if not self._db_engine:
            self._db_engine = sqlalchemy.create_engine('sqlite://')
            sql_file = os.path.join(os.path.dirname(__file__), 'test_db.sql')
            with open(sql_file, "rt") as f:
                sql_text = f.read()
                for statement in sql_text.split(';'):
                    self._db_engine.execute(statement)
        return self._db_engine

    def test_db_create(self):
        # Should execute without errors
        engine = self.get_db_engine()
        meta = sqlalchemy.MetaData()
        meta.reflect(bind=engine)
        self.assertGreater(len(meta.tables), 1, "It is expected that more than one table reflected.")


    @patch('sys.argv')
    def test_doc(self, mock_argv):
        self._delete_test_folder()
        output_folder = self._get_output_folder()
        def getitem(a, b, **kwargs):
            return ['-o{}'.format(output_folder), '-usqllite://']
        mock_argv.__getitem__ = getitem

        engine = self.get_db_engine()
        with patch('sqlalchemy.create_engine') as mock_create_engine:
            mock_create_engine.return_value = engine
            exit_code = schemadoc.doc.main()
            self.assertEqual(exit_code, 0)
