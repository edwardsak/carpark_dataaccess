from datalayer.models.models import CarMovement

from google.appengine.ext import ndb

class CarMovementDataAccess():
    def create(self, vm):
        movement_code = CarMovement.get_movement_code(vm.car_reg_no, vm.movement_date)
        
        data = CarMovement(parent=ndb.Key('Car', vm.car_reg_no), id=movement_code)
        data.movement_code = movement_code
        data.car_reg_no = vm.car_reg_no
        data.movement_date = vm.movement_date
        data.bf_amt = vm.bf_amt
        data.register_amt = vm.register_amt
        data.top_up_amt = vm.top_up_amt
        data.charge_amt = vm.charge_amt
        data.bal_amt = vm.bal_amt
        data.put()
    
    def delete(self, movement_date):
        q = CarMovement.query(CarMovement.movement_date==movement_date)
        mvs = q.fetch()
        
        for mv in mvs:
            mv.key.delete()