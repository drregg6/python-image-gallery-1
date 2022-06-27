from gallery.data.image import Image
from gallery.data.image_dao import ImageDao
from gallery.data.s3 import add_image, get_image, delete_image
from gallery.data import db

class PostgresImageDAO(ImageDao):
    def __init__(self):
        pass

    def get_images(self, username):
        images = []
        cursor = db.execute("select image_id, path, username, image_name from images where username=%s", (username,))
        for t in cursor.fetchall():
            images.append(Image(t[0], t[1], t[2], t[3]))
        return images
   
    def get_image(self, username, image_name):
        cursor = db.execute("select image_id, path, username, image_name from images where username=%s and image_name=%s", (username, image_name))
        temp = cursor.fetchone()
        if temp is None:
            return None
        else:
            res = Image(temp[0], temp[1], temp[2], temp[3])
        return res

    def add_image(self, username, image, path):
        db.execute("insert into images (path, username, image_name) values (%s, %s, %s)", (path, username, image.filename))
        add_image(image, path)

    def delete_image(self, image):
        db.execute("delete from images where image_id=%s", (image.image_id,))
        delete_image(image.path)
