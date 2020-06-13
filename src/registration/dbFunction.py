import hashlib
import pymongo


class UserTableHandler:
    def __init__(self, app, userType="user"):
        self.logger = app.logger
        myclient = pymongo.MongoClient('mongodb://mongo:27017/')
        self.logger.info("server version:", myclient.server_info()["version"])
        mydb = myclient["UserDb"]
        if userType.lower().capitalize() == "User" or "Admin":
            self.table = mydb[userType]
        else:
            self.table = mydb["user"]

    def add(self, login, password):
        if self.table.find_one({"login": login}) is None:
            user = {"login": login,
                    "password": hashlib.sha512(password.encode("utf-8")).hexdigest()
                    }
            self.table.insert_one(user)
            return 1
        return 0

    def modify(self, login, attributeType, newAttribute):
        myquery = {"login": login}
        user = self.table.find_one(myquery)
        if user is not None:
            if attributeType == "password":
                newvalues = {"$set": {"password": hashlib.sha512(newAttribute.encode("utf-8")).hexdigest()}}
                self.table.update_one(myquery, newvalues)
                return 1
        return 0

    def delete(self, login, password):
        user = self.table.find_one({"login": login})
        if user is not None and user["password"] == hashlib.sha512(password.encode("utf-8")).hexdigest():
            self.table.delete_one({"login": login})
            return 1
        return 0
