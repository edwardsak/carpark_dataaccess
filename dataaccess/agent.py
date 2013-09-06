from datalayer.models.models import Agent
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class AgentDataAccess():
    def get(self, code):
        return Agent.query(ancestor=ndb.Key('Agent', code)).get()
    
    def create(self, vm):
        self.__create(vm)
    
    @ndb.transactional(xg=True)
    def __create(self, vm):
        # validate id
        data_validate = self.get(vm.code)
        if data_validate != None:
            raise Exception('Agent ID already exist.')
        
        data = Agent(parent=ndb.Key('Agent', vm.code), id=vm.code)
        data.code = vm.code
        data.name = vm.name
        data.pwd = vm.pwd
        data.account_type = vm.account_type
        data.address = vm.address
        data.tel = vm.tel
        data.hp = vm.hp
        data.email = vm.email
        data.comm_per = vm.comm_per
        data.bal_amt = vm.bal_amt
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
            raise Exception('Agent not found.')
        
        # validate lastModified
        if data.last_modified != vm.last_modified:
            raise Exception('Record has been modified by other user.')
        
        data.name = vm.name
        data.account_type = vm.account_type
        data.address = vm.address
        data.tel = vm.tel
        data.hp = vm.hp
        data.email = vm.email
        data.comm_per = vm.comm_per
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
            raise Exception('Agent not found.')
        
        data.pwd = vm.pwd
        data.put()
        
        
    def change_pwd(self, vm):
        self.__change_pwd(vm)
    
    @ndb.transactional(xg=True)
    def __change_pwd(self, vm):
        # validate id
        data = self.get(vm.code)
        if data == None:
            raise Exception('Agent not found.')
        
        if data.pwd != vm.old_pwd:
            raise Exception('Incorrect password.')
        
        data.pwd = vm.pwd
        data.put()