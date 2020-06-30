from unittest import TestCase
import data_objects as do
import database
import my_secrets


class TestDatabase(TestCase):
    def test_create_tables(self):
        db = database.DatabaseAccess(my_secrets.db_user, my_secrets.db_pass)
        db.create_tables()
        self.assertTrue(True)

    def test_insert_update_get_delete_user(self):
        db = database.DatabaseAccess(my_secrets.db_user, my_secrets.db_pass)
        user = do.User('User1', 'user1@mail.ru', 'qwerqwer', 740, 20)
        user_id = db.insert_user(user)
        self.assertTrue(user_id > 0)
        user.score = 750
        self.assertEqual(user_id, db.update_user(user_id, user))
        self.assertEqual(user, db.get_user(user_id))
        db.delete_user(user_id)
        self.assertEqual(db.get_user(user_id), None)
