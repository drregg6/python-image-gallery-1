from gallery.data.image import Image
from gallery.data.image_dao import ImageDao
from gallery.data.s3 import add_image, get_image
from gallery.data import db

class PostgresImageDAO(ImageDao):
    def __init__(self):
        pass

    def get_images(self, username):
        res = []
        cursor = db.execute("select image_id, path, username from images where username=%s", (username,))
        for t in cursor.fetchall():
            res.append(Image(t[0], t[1], t[2]))
        return res;
    
    def add_image(self, username, file_name, path):
        db.execute("insert into images (path, username) values (%s, %s)", (path, username))
        add_image(file_name, path)
