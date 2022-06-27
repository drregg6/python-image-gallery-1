class Image():
    def __init__(self, image_id, path, owner, image_name):
        self.image_id = image_id
        self.path = path
        self.owner = owner
        self.image_name = image_name
        self.url = "https://s3.amazonaws.com/edu.au.cc.dzr-0056.image-gallery-2/" + path

        def __repr__(self):
            return "id=>" + self.image_id + " path=>" + self.path + " owner=>" + self.owner + " url=>" + self.url
