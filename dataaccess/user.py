from datalayer.models.models import User

class UserDataAccess():
    def create(self, vm):
        data = User()
        data.code = vm.code
        data.name = vm.name
        data.pwd = vm.pwd
        data.put()