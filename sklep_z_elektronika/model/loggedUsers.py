class LoggedUsers:
    def __init__(self):
        self.loggedClients = dict()
        self.loggedEmployees = dict()

    def addLoggedClient(self, clientID, client):
        self.loggedClients[clientID] = client

    def removeLoggedClient(self, clientID):
        self.loggedClients.pop(clientID)

    def getLoggedClient(self, clientID):
        return self.loggedClients.get(clientID)

    def addLoggedEmployee(self, employeeID, employee):
        self.loggedEmployees[employeeID] = employee

    def removeLoggedEmployee(self, employeeID):
        self.loggedEmployees.pop(employeeID)

    def getLoggedEmployee(self, employeeID):
        return self.loggedEmployees.get(employeeID)
