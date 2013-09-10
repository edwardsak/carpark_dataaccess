from datalayer.models.models import Customer
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class CustomerDataAccess():
    def get(self, ic):
        return Customer.query(ancestor=ndb.Key('Customer', ic)).get()
    
    def create(self, vm):
        # validate id
        data_validate = self.get(vm.ic)
        if data_validate != None:
            raise Exception('IC/PP No. already exist.')
        
        data = Customer(parent=ndb.Key('Customer', vm.ic), id=vm.ic)
        data.ic = vm.ic
        data.name = vm.name
        data.address = vm.address
        data.tel = vm.tel
        data.hp = vm.hp
        data.email = vm.email
        # default password is ic
        data.pwd = vm.ic
        data.active = True
        data.last_modified = str(DateTime.malaysia_now())
        data.put()
        
        return data
        
    def update(self, vm):
        return self.__update(vm)
    
    @ndb.transactional(xg=True)
    def __update(self, vm):
        # get data
        data = self.get(vm.ic)
        if data == None:
            raise Exception('Customer not found.')
        
        # validate lastModified
        if data.last_modified != vm.last_modified:
            raise Exception('Record has been modified by other user.')
        
        data.name = vm.name
        data.address = vm.address
        data.tel = vm.tel
        data.hp = vm.hp
        data.email = vm.email
        data.active = vm.active
        data.last_modified = str(DateTime.malaysia_now())
        data.put()
        
        return data
    
    def save_register(self, vm):
        customer = self.get(vm.ic)
        if customer:
            # update
            pass
        else:
            # create
            customer = self.create(vm)
            
        return customer
    
    def reset_pwd(self, vm):
        self.__reset_pwd(vm)
    
    @ndb.transactional(xg=True)
    def __reset_pwd(self, vm):
        # get data
        data = self.get(vm.ic)
        if data == None:
            raise Exception('Customer not found.')
        
        data.pwd = vm.pwd
        data.put()
    
    def change_pwd(self, vm):
        self.__change_pwd(vm)
    
    @ndb.transactional(xg=True)
    def __change_pwd(self, vm):
        # validate id
        data = self.get(vm.ic)
        if data == None:
            raise Exception('Customer not found.')
        
        if data.pwd != vm.old_pwd:
            raise Exception('Incorrect password.')
        
        data.pwd = vm.pwd
        data.put()