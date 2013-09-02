from datalayer.models.models import User

class UserDataAccess():
    def create(self, obj):
        user = User()
        user.code = obj.code
        user.name = obj.name
        user.pwd = obj.pwd
        user.put()