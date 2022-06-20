from gallery.data.user_dao import UserDAO
from gallery.data import db
from gallery.data.user import User

class PostgresUserDAO(UserDAO):
    def __init__(self):
        pass

    def get_users(self):
        res = []
        cursor = db.execute("select username,password,full_name from users")
        for t in cursor.fetchall():
            res.append(User(t[0], t[1], t[2]))
        return res
    
    def get_user(self, username):
        username = username.lower()
        cursor = db.execute("select username,password,full_name from users where username=%s", (username,))
        temp = cursor.fetchone()
        res = User(temp[0], temp[1], temp[2])

        return res

    def delete_user(self, username):
        username = username.lower()
        db.execute("delete from users where username=%s", (username,))

    def create_user(self, username, password, full_name):
        username = username.lower()
        db.execute("insert into users (username, password, full_name) values (%s, %s, %s)", (username, password, full_name))

    def modify_user(self, username, password, full_name):
        username = username.lower()
        db.execute("update users set password = %s, full_name = %s where username = %s", (password, full_name, username))
