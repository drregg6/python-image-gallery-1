class User:
    def __init__(self, username, password, full_name):
        self.username = username
        self.password = password
        self.full_name = full_name

    def __repr__(self):
        return self.full_name + " (" + self.username + "): " + self.password
