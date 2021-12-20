from sklep_z_elektronika.model.loggedUsers import LoggedUsers


class UserController:
    def __init__(self):
        self.loggedUsers = LoggedUsers()

    def login(self, username, password):
        user = None
        #tu sie bedzie cos dzialo
        #typu stored procedure login
        #i na koncu dodanie go do zalogowanych
        self.loggedUsers.addLoggedUser(user)

    def logout(self, userID):
        user = None
        # tu sie bedzie cos dzialo
        # i na koncu wylogowanie
        self.loggedUsers.removeLoggedUser(user)