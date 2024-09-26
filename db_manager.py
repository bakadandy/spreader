import sqlite3
class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

    def add_user(self):

