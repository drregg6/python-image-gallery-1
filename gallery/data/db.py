import psycopg2
import json
from gallery.data.secrets import get_secret_image_gallery

connection = None

def get_secret():
    json_string = get_secret_image_gallery()
    return json.loads(json_string)

def connect():
    print('connecting...')
    global connection
    secret = get_secret()
    print('got secret')
    connection = psycopg2.connect(host=secret['host'], dbname=secret['database_name'], user=secret['username'], password=secret['password'])
    print('connected')

def execute(query, args=None):
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    connection.commit()
    return cursor
