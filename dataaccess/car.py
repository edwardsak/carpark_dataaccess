from datalayer.models.models import Car
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class CarDataAccess():
    def get(self, reg_no):
        return Car.query(ancestor=ndb.Key('Car', reg_no)).get()
    
    def create(self, vm):
        # validate id
        data_validate = self.get(vm.reg_no)
        if data_validate != None:
            raise Exception('Car Reg. No. already exist.')
        
        data = Car(id=vm.reg_no)
        data.reg_no = vm.reg_no
        data.customer_ic = vm.customer_ic
        data.customer = vm.customer.key
        data.bal_amt = vm.bal_amt   # register may be RM10
        data.active = True
        data.last_modified = str(DateTime.malaysia_now())
        data.put()
        
        return data
        
    def update(self, vm):
        return self.__update(vm)
    
    @ndb.transactional(xg=True)
    def __update(self, vm):
        # get data
        data = self.get(vm.reg_no)
        if data == None:
            raise Exception('Car not found.')
        
        # validate lastModified
        if data.last_modified != vm.last_modified:
            raise Exception('Record has been modified by other user.')
        
        data.active = vm.active
        data.last_modified = str(DateTime.malaysia_now())
        data.put()
        
        return data
    
    def save_register(self, vm):
        car = self.get(vm.reg_no)
        if car:
            # update car bal amt
            car.bal_amt += vm.bal_amt
            car.put()
        else:
            # create car
            car = self.create(vm)
            
        return car