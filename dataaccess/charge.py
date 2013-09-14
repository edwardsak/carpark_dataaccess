from datalayer.models.models import Charge, Attendant
from datalayer.viewmodels.viewmodels import TranViewModel, CarViewModel
from datalayer.dataaccess.basetran import BaseTranDataAccess
from datalayer.dataaccess.master import MasterDataAccess
from datalayer.dataaccess.tran import TranDataAccess
from datalayer.dataaccess.attendant import AttendantDataAccess
from datalayer.dataaccess.car import CarDataAccess
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class ChargeDataAccess(BaseTranDataAccess):
    def get_key(self, tran_date, attendant_code=None, tran_code=None):
        return self._BaseTranDataAccess__get_key(
                            Charge, tran_date,
                            Attendant, attendant_code, 
                            tran_code
                            )
    
    def get(self, tran_date, attendant_code, tran_code):
        key = self.get_key(tran_date, attendant_code, tran_code)
        return Charge.query(ancestor=key).get()
    
    def fetch(self, tran_date, attendant_code=None, tran_code=None):
        key = self.get_key(tran_date, attendant_code, tran_code)
        return Charge.query(ancestor=key).fetch()
        
    def create(self, vm):
        # get attendant
        attendant_da = AttendantDataAccess()
        attendant = attendant_da.get(vm.attendant_code)
        if attendant is None:
            raise Exception('Attendant not found.')
        
        vm.attendant = attendant
        
        # get car
        car_da = CarDataAccess()
        car = car_da.get(vm.car_reg_no)
        if car is None:
            # if car not found, create car
            car_vm = CarViewModel()
            car_vm.reg_no = vm.car_reg_no
            
            car_da = CarDataAccess()
            car = car_da.create(car_vm)
            
        vm.car = car
        
        self.__create(vm)
    
    @ndb.transactional(xg=True)
    def __create(self, vm):
        # get master seq
        master_da = MasterDataAccess()
        master = master_da.get('Charge')
        master.seq += 1
        master.put()
        
        # insert deposit
        tran_code = Charge.get_tran_code(master.seq)
        vm.tran_code = tran_code
        
        data = Charge(
                     parent=self.get_key(vm.tran_date, vm.attendant_code), 
                     id=tran_code
                     )
        data.tran_code = tran_code
        data.tran_type = vm.tran_type
        data.tran_date = vm.tran_date
        data.seq = master.seq
        data.remark = vm.remark
        
        data.attendant_code = vm.attendant_code
        data.attendant = vm.attendant.key
        data.lot_no = vm.lot_no
        data.car_reg_no = vm.car_reg_no
        data.car = vm.car.key
        
        data.start_time = vm.start_time
        data.charge_time = vm.charge_time
        data.duration = vm.duration
        data.sub_total = vm.sub_total
        data.comm_per = vm.comm_per
        data.comm_amt = vm.comm_amt
        data.amt = vm.amt
        data.ended = False
        
        data.created_by = ''
        data.created_date = DateTime.malaysia_now()
        data.modified_by = ''
        data.modified_date = None
        data.void_by = ''
        data.void_date = None
        data.void = False
        data.last_modified = str(data.created_date)
        data.put()
        
        # insert tran
        tran_obj = TranViewModel()
        tran_obj.tran_code = data.tran_code
        tran_obj.tran_date = data.tran_date
        tran_obj.tran_type = data.tran_type
        tran_obj.car_reg_no = data.car_reg_no
        
        tran_da = TranDataAccess()
        tran_da.create(tran_obj)
        
        # update car bal amt
        self.__update_car_bal_amt(vm.car_reg_no, vm.sub_total)
        
    @ndb.transactional(xg=True)
    def update_charge(self, vm):
        charge = self.get(vm.tran_date, vm.attendant_code, vm.tran_code)
        if charge is None:
            raise Exception("Charge not found.")
        
        old_amt = charge.amt
        
        charge.sub_total = vm.sub_total
        charge.comm_per = vm.comm_per
        charge.comm_amt = vm.comm_amt
        charge.amt = vm.amt
        charge.charge_time = vm.charge_time
        charge.put()
        
        # update car bal amt
        self.__update_car_bal_amt(vm.car_reg_no, vm.sub_total - old_amt)
        
    def __update_car_bal_amt(self, car_reg_no, amt):
        car_da = CarDataAccess()
        car = car_da.get(car_reg_no)
        car.bal_amt -= amt
        car.bal_amt = round(car.bal_amt, 2)
        car.put()
        
    @ndb.transactional(xg=True)
    def end(self, vm):
        charge = self.get(vm.tran_date, vm.attendant_code, vm.tran_code)
        if charge is None:
            raise Exception("Charge not found.")
        
        charge.ended = True
        charge.put()