import sqlite3


class DataBase:
    def __init__(self):
        con = self.con = sqlite3.connect('notes.db')
        cur = self.cur = con.cursor()
        tables = self.tables = cur.execute(
            "SELECT name FROM sqlite_master").fetchall()
        if ('notes', ) not in tables:
            cur.execute(
                "CREATE TABLE notes(user_id, list, note, add_time, done_time)")
        if ('menus', ) not in tables:
            cur.execute("CREATE TABLE menus(user_id, username, menu)")
        con.commit()

    def register(self, user):
        menu = "default"
        self.cur.execute("INSERT INTO menus VALUES(?, ?, ?)",
                         (user.id, user.username,  menu))
        self.con.commit()
        return menu

    def get_menu(self, user_id):
        exec = self.cur.execute("""SELECT menu
                            FROM menus
                            WHERE user_id = ?""",
                                (user_id, ))

        res = exec.fetchone()
        return None if res is None else res[0]

    def get_user_id(self, user_id):
        exec = self.cur.execute("""SELECT user_id
                            FROM menus
                            WHERE username = ?""",
                                (user_id, ))

        res = exec.fetchone()
        return None if res is None else res[0]

    def set_menu(self, user_id, menu):
        self.cur.execute("""UPDATE menus
                    SET menu = ?
                    WHERE user_id = ?""", (menu, user_id))
        self.con.commit()

    def reset_all_notes(self, user_id):
        self.cur.execute("""DELETE FROM notes
                    WHERE user_id = ?""", (user_id, ))
        self.con.commit()

    def get_list(self, user_id, list_name):
        exec = self.cur.execute("""SELECT note, add_time, done_time
                            FROM notes
                            WHERE user_id = ? AND list = ? 
                            ORDER BY add_time""",
                                (user_id, list_name))
        return exec.fetchall()

    def get_all_notes(self, user_id):
        exec = self.cur.execute("""SELECT note, add_time, done_time
                            FROM notes
                            WHERE user_id = ?
                            ORDER BY add_time""",
                                (user_id, ))
        return exec.fetchall()

    def insert_note(self, user_id, list_name, note, timestamp):
        data = (user_id, list_name, note, timestamp, 0)
        self.cur.execute("INSERT INTO notes VALUES(?, ?, ?, ?, ?)", data)
        self.con.commit()

    def delete_note(self, user_id, list_name=None, pos=None, values=None, timestamp=None):
        if timestamp is None:
            if values is None:
                values = self.get_list(user_id, list_name)
            item = values[pos - 1]
            timestamp = item[1]
        self.cur.execute("""DELETE 
                    FROM notes
                    WHERE user_id = ? AND add_time = ?""",
                         (user_id, timestamp))
        self.con.commit()

    def set_done_time(self, user_id, done_time, list_name=None, pos=None, values=None, timestamp=None):
        if timestamp is None:
            if values is None:
                values = self.get_list(user_id, list_name)
            timestamp = values[pos - 1][1]
        self.cur.execute("""UPDATE notes
                    SET done_time = ?
                    WHERE user_id = ? AND add_time = ?""", (done_time, user_id, timestamp))
        self.con.commit()
