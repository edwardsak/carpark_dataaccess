from datalayer.dataaccess.user import UserDataAccess
from datalayer.models.models import User

class UserAppService():
    def create(self, vm):
        da = UserDataAccess()
        da.create(vm)