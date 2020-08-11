class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User:{self.username}>'

users = []
users.append(User(id=1, username="Nohax", password='paladin'))
users.append(User(id=4, username='Bob', password='123456'))