class UserLogin():
    def fromBD(self, userID, DB):
        self.__user=DB.getUserID(userID)
        return self

    def is_authenticated(self):
        try:
            self.get_id()
            return True
        except:
            return False


    def is_active(self):
        return True

    def is_anonnymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])

    def get_user(self):
        return self.__user

    def createUser(self, user):
        self.__user = user
        return self