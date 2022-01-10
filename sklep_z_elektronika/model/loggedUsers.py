class LoggedUsers:
    def __init__(self):
        self.loggedClients = dict()
        self.loggedEmployees = dict()

    def addLoggedClient(self, clientID, client):
        print("xd login")
        self.loggedClients[clientID] = client

    def removeLoggedClient(self, clientID):
        print("xd logout")
        self.loggedClients.pop(clientID)

    def getLoggedClient(self, clientID):
        return self.loggedClients.get(clientID)

    def checkIfLogged(self, clientID):
        return clientID in self.loggedClients

    def checkIfEmpLogged(self, employeeID):
        return employeeID in self.loggedEmployees       # zwraca True lub False

    def addLoggedEmployee(self, employeeID, employee):
        self.loggedEmployees[employeeID] = employee

    def removeLoggedEmployee(self, employeeID):
        self.loggedEmployees.pop(employeeID)

    def getLoggedEmployee(self, employeeID):
        return self.loggedEmployees.get(employeeID)
