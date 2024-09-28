import sqlite3

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
    def add_user(self, username, password):
        self.cursor.execute(f"INSERT INTO users(username, password) VALUES('{username}', '{password}')")
        res = self.cursor.execute(f"SELECT id FROM users WHERE username = '{username}'")
        old_id = res.fetchone()
        self.cursor.execute(f"INSERT INTO stats VALUES({old_id}, 0, 0)")
        return "user added successfully"

    def update_stat(self, id, wm_rating, score):
        try:
            res = self.cursor.execute(f"SELECT wm_rating, score FROM stats WHERE id = {id}")

            old_wm_rating, old_score = res.fetchone()
            if (old_wm_rating == None or old_score == None):
                return "user not found"

            else:
                new_wm_rating = max(wm_rating, old_wm_rating)
                new_score = score + old_score

                self.cursor.execute(f"UPDATE users SET wm_rating={new_wm_rating}, score={new_score} WHERE id = {id}")
                return "stats updated successfully"

        except Exception as e:
            return f"Error occured, {e}"

    def login_check(self, username, password):
        res = self.cursor.execute(f"SELECT id FROM users WHERE username = {username} AND password = {password}")
        id = res.fetchone()
        if id == None:
            return "Incorrect username or password"
        else:
            return "Successful login"
    def receive_stats(self, id):
        res = self.cursor.execute(f"SELECT wm_rating, score FROM stats WHERE id = {id}")
        wm_rating, score = res.fetchone()
        if wm_rating == None or score == None:
            return "Incorrect id"
        else:
            return wm_rating, score

