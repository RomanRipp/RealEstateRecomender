from unittest import TestCase
import data_objects as do
import database
import my_secrets


class TestDatabase(TestCase):
    def test_create_tables(self):
        db = database.DatabaseAccess(my_secrets.db_user, my_secrets.db_pass, database="test")
        db.create_tables()
        self.assertTrue(True)

    def test_insert_update_get_delete_user(self):
        db = database.DatabaseAccess(my_secrets.db_user, my_secrets.db_pass, database="test")
        user = do.User('user userovich', 'user@mail.ru', 740, 20)
        user.set_password('qwerqwer')
        user_id = db.insert_user(user)
        self.assertTrue(user_id > 0)
        user.score = 750
        self.assertEqual(user_id, db.update_user(user_id, user))
        db_user = db.find_user(user_id)
        self.assertEqual(user.name, db_user.name)
        self.assertEqual(user.score, db_user.score)
        db.delete_user(user_id)
        self.assertEqual(db.find_user(user_id), None)
