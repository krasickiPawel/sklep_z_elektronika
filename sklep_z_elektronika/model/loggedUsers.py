class LoggedUsers:
    def __init__(self):
        self.loggedUsers = dict()

    def addLoggedUser(self, userID, user):
        self.loggedUsers[userID] = user

    def removeLoggedUser(self, userID):
        self.loggedUsers.pop(userID)

    def getLoggedUser(self, userID):
        return self.loggedUsers.get(userID)
