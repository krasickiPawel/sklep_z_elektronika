class LoggedUsers:
    def __init__(self):
        self.loggedUsers = []

    def addLoggedUser(self, user):
        self.loggedUsers.append(user)

    def removeLoggedUser(self, user):
        self.loggedUsers.remove(user)
