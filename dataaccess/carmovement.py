from datalayer.models.models import CarMovement, AgentMovement, Car

class CarMovementDataAccess():
    def get_key(self, movement_date, car_reg_no=None, movement_code=None):
        return AgentMovement.get_key(
                                     CarMovement, movement_date, 
                                     Car, car_reg_no, 
                                     movement_code
                                     )
    
    def get(self, movement_date, car_reg_no, movement_code):
        key = self.get_key(movement_date, car_reg_no, movement_code)
        return CarMovement.query(ancestor=key).get()
            
    def fetch(self, movement_date, car_reg_no=None, movement_code=None):
        key = self.get_key(movement_date, car_reg_no, movement_code)
        return CarMovement.query(ancestor=key).fetch()
    
    def create(self, vm):
        movement_code = CarMovement.get_movement_code(vm.car_reg_no, vm.movement_date)
        
        data = CarMovement(
                           parent=self.get_key(vm.movement_date, vm.car_reg_no), 
                           id=movement_code
                           )
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
        mvs = self.fetch(movement_date)
        
        for mv in mvs:
            mv.key.delete()