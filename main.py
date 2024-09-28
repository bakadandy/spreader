#import sqlite3
import sys
import GUI
from PyQt5.QtWidgets import QApplication
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI.LoginWindow()
    window.show()
    sys.exit(app.exec_())
# def create_table():
#     conn = sqlite3.connect("users.db")
#     cur = conn.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
#     conn.commit()
#     conn.close()
#
# create_table()