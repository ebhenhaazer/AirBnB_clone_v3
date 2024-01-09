#!/usr/bin/python3
'''
    Testing the file_storage module.
'''
import time
import unittest
import sys
from models.engine.db_storage import DBStorage
from models import storage
from models.user import User
from models.state import State
from models import storage
from console import HBNBCommand
from os import getenv
from io import StringIO

db = getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db != 'db', "Testing DBstorage only")
class test_DBStorage(unittest.TestCase):
    '''
        Testing the DB_Storage class
    '''
    @classmethod
    def setUpClass(cls):
        '''
            Initializing classes
        '''
        cls.dbstorage = DBStorage()
        cls.output = StringIO()
        sys.stdout = cls.output

    @classmethod
    def tearDownClass(cls):
        '''
            delete variables
        '''
        del cls.dbstorage
        del cls.output

    def create(self):
        '''
            Create HBNBCommand()
        '''
        return HBNBCommand()

    def test_new(self):
        '''
            Test DB new
        '''
        new_obj = State(name="California")
        self.assertEqual(new_obj.name, "California")

    def test_dbstorage_user_attr(self):
        '''
            Testing User attributes
        '''
        new = User(email="melissa@hbtn.com", password="hello")
        self.assertTrue(new.email, "melissa@hbtn.com")

    def test_dbstorage_check_method(self):
        '''
            Check methods exists
        '''
        self.assertTrue(hasattr(self.dbstorage, "all"))
        self.assertTrue(hasattr(self.dbstorage, "__init__"))
        self.assertTrue(hasattr(self.dbstorage, "new"))
        self.assertTrue(hasattr(self.dbstorage, "save"))
        self.assertTrue(hasattr(self.dbstorage, "delete"))
        self.assertTrue(hasattr(self.dbstorage, "reload"))

    def test_dbstorage_all(self):
        '''
            Testing all function
        '''
        storage.reload()
        result = storage.all("")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
        new = User(email="adriel@hbtn.com", password="abc")
        console = self.create()
        console.onecmd("create State name=California")
        result = storage.all("State")
        self.assertTrue(len(result) > 0)

    def test_dbstorage_new_save(self):
        '''
           Testing save method
        '''
        new_state = State(name="NewYork")
        storage.new(new_state)
        save_id = new_state.id
        result = storage.all("State")
        temp_list = []
        for k, v in result.items():
            temp_list.append(k.split('.')[1])
            obj = v
        self.assertTrue(save_id in temp_list)
        self.assertIsInstance(obj, State)

    def test_get(self):
        '''
            Testing Get Method
        '''
        new_user1 = User(email="dragonballs@anime.com", password="wishes",
                         first_name="Gouku", last_name="Saiyan")
        storage.new(new_user1)
        save_id = new_user1.id
        storage.save
        get_user = storage.get('User', save_id)
        self.assertEqual(new_user1.id, get_user.id)
        self.assertTrue(isinstance(get_user, User))
        get_none = storage.get('User', 'no id')
        self.assertTrue(get_none is None)

    def test_dbstorage_delete_and_count(self):
        '''
            Testing delete and count method
        '''
        new_user = User(email="haha@hehe.com", password="abc",
                        first_name="Adriel", last_name="Tolentino")
        storage.new(new_user)
        save_id = new_user.id
        key = "User.{}".format(save_id)
        self.assertIsInstance(new_user, User)
        storage.save()
        old_result = storage.all("User")
        del_user_obj = old_result[key]
        self.assertEqual(storage.count('User'), 1)
        self.assertGreaterEqual(storage.count(), storage.count('User'))
        storage.delete(del_user_obj)
        new_result = storage.all("User")
        self.assertNotEqual(len(old_result), len(new_result))
        self.assertEqual(storage.count('User'), 0)
        self.assertEqual(storage.count(), 1)

    def test_raise(self):
        '''
           Test for Exception errors
        '''
        self.assertRaises(TypeError, storage.get, None)

    def test_model_storage(self):
        '''
            Test to check if storage is an instance for DBStorage
        '''
        self.assertTrue(isinstance(storage, DBStorage))
