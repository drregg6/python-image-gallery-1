import psycopg2
import json
from secrets import get_secret_image_gallery

def read_secret_from_aws():
    json_string = get_secret_image_gallery()
    return json.loads(json_string)


def get_password(secret):
    return secret['password']


def get_host(secret):
    return secret['host']


def get_username(secret):
    return secret['username']


def get_dbname(secret):
    return secret['database_name']


class DbConnection:
    secret = None

    def __init__(self):
        self.connection = None

    def connect(self):
        secret = read_secret_from_aws()
        print(secret)
        self.connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))

    # cursor.execute will execute a query
    def execute(self, query, args=None):
        cursor = self.connection.cursor()
        # no arguments, just execute
        if not args:
            cursor.execute(query)
        # execute with arguments
        else:
            cursor.execute(query, args)
        return cursor

    def get_users(self):
        cursor = self.connection.cursor()
        cursor.execute('select * from users')
        s = '\n';
        s += 'username   |   password   |   full_name'
        s += '\n--------------------------------------------'
        for row in cursor:
            s += '\n'
            for item in row:
                s += item + '   |   '
        return s

    def get_user(self, username):
        cursor = self.connection.cursor()
        username = username.lower()
        query = 'select * from users where username = \'%s\'' % username
        cursor.execute(query)
        s = ''
        for row in cursor:
            s += '\n'
            for item in row:
                s += item + ','
        return s

    def add_user(self, username, password, full_name):
        username = username.lower()
        cursor = self.connection.cursor()
        query = 'insert into users (username, password, full_name) values (%s, %s, %s)'
        cursor.execute(query, (username, password, full_name))
        self.connection.commit()

    def update_user(self, username, password, full_name):
        username = username.lower()
        cursor = self.connection.cursor()
        query = 'update users set password = %s, full_name = %s where username = %s'
        cursor.execute(query, (password, full_name, username))
        self.connection.commit()

    def delete_user(self, username):
        cursor = self.connection.cursor()
        username = username.lower()
        query = 'delete from users where username = \'%s\'' % username
        cursor.execute(query)
        self.connection.commit()


def main():
    db = DbConnection()
    db.connect()
    res = db.execute('select * from users')
    for row in res:
        print(row)
    db.add_user('dave', 'simple', 'dave regg')

if __name__ == '__main__':
    main()
