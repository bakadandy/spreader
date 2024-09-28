import sqlite3

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
    def add_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users(username, password) VALUES(?, ?)", (username, password))
            self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            id_tuple = self.cursor.fetchone()

            # Extract the actual id from the tuple
            id = id_tuple[0]

            self.cursor.execute("INSERT INTO stats VALUES(?, ?, ?)", (id, 0, 0))
            print("Қолданушы тіркелді")
            return "Қолданушы тіркелді"
        except Exception as e:
            print(e)

    def update_stat(self, id, wm_rating, score):
        try:
            res = self.cursor.execute("SELECT wm_rating, score FROM stats WHERE id = ?", (id))

            old_wm_rating, old_score = res.fetchone()
            if (old_wm_rating == None or old_score == None):
                print("Колданушы табылмады")
                return "Қолданушы табылмады"

            else:
                new_wm_rating = max(wm_rating, old_wm_rating)
                new_score = score + old_score

                self.cursor.execute(
                    "UPDATE stats SET wm_rating = ?, score = ? WHERE id = ?",
                    (new_wm_rating, new_score, id)
                )
                print("Көрсеткіштер жаңартылды")
                return "Көрсеткіштер жаңартылды"

        except Exception as e:
            print(e)
            return f"Error occured, {e}"

    def login_check(self, username, password):
        self.cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()  # fetchone() returns None if no result is found

        if user is None:
            print("Колданушы табылмады")
            return "Кұпиясөз немесе қолданушы аты дұрыс емес"
        else:
            print("Колданушы табылды")
            return "Тіркелу орындалды"
    def receive_stats(self, id):
        self.cursor.execute("SELECT wm_rating, score FROM stats WHERE id = ?", (id,))
        result = self.cursor.fetchone()

        # Check if result is None (no user found)
        if result is None:
            print("Колданушы табылмады")
            return "Id дұрыс емес"
        else:
            # Unpack wm_rating and score from the result tuple
            wm_rating, score = result
            print("Колданушы табылды")
            return wm_rating, score