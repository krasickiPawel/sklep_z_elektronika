from datetime import datetime


class Database:
    def __init__(self, host, user, password, database):
        self.db = None
        self.cursor = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database






