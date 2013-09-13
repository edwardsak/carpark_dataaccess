from datalayer.models.models import User
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class UserDataAccess():
    def get(self, code):
        return User.query(ancestor=ndb.Key('User', code)).get()
    
    def create(self, vm):
        self.__create(vm)
    
    @ndb.transactional(xg=True)
    def __create(self, vm):
        # validate id
        data_validate = self.get(vm.code)
        if data_validate != None:
            raise Exception('User ID already exist.')
        
        data = User(id=vm.code)
        data.code = vm.code
        data.name = vm.name
        data.pwd = vm.pwd
        data.level = vm.level
        data.active = vm.active
        data.last_modified = str(DateTime.malaysia_now())
        data.put()
        
        
    def update(self, vm):
        self.__update(vm)
    
    @ndb.transactional(xg=True)
    def __update(self, vm):
        # get data
        data = self.get(vm.code)
        if data == None:
            raise Exception('User not found.')
        
        # validate lastModified
        if data.last_modified != vm.last_modified:
            raise Exception('Record has been modified by other user.')
        
        data.name = vm.name
        data.level = vm.level
        data.active = vm.active
        data.last_modified = str(DateTime.malaysia_now())
        data.put()
        
    def reset_pwd(self, vm):
        self.__reset_pwd(vm)
    
    @ndb.transactional(xg=True)
    def __reset_pwd(self, vm):
        # get data
        data = self.get(vm.code)
        if data == None:
            raise Exception('User not found.')
        
        data.pwd = vm.pwd
        data.put()
        
        
    def change_pwd(self, vm):
        self.__change_pwd(vm)
    
    @ndb.transactional(xg=True)
    def __change_pwd(self, vm):
        # validate id
        data = self.get(vm.code)
        if data == None:
            raise Exception('User not found.')
        
        if data.pwd != vm.old_pwd:
            raise Exception('Incorrect password.')
        
        data.pwd = vm.pwd
        data.put()