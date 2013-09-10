from datalayer.models.models import AgentMovement, Agent

class AgentMovementDataAccess():
    def get_key(self, movement_date, agent_code=None, movement_code=None):
        return AgentMovement.get_key(
                                     AgentMovement, movement_date, 
                                     Agent, agent_code, 
                                     movement_code
                                     )
    
    def get(self, movement_date, agent_code, movement_code):
        key = self.get_key(movement_date, agent_code, movement_code)
        return AgentMovement.query(ancestor=key).get()
            
    def fetch(self, movement_date, agent_code=None, movement_code=None):
        key = self.get_key(movement_date, agent_code, movement_code)
        return AgentMovement.query(ancestor=key).fetch()
    
    def create(self, vm):
        movement_code = AgentMovement.get_movement_code(vm.agent_code, vm.movement_date)
        
        data = AgentMovement(
                             parent=self.get_key(vm.movement_date, vm.agent_code), 
                             id=movement_code
                             )
        data.movement_code = movement_code
        data.agent_code = vm.agent_code
        data.movement_date = vm.movement_date
        data.bf_amt = vm.bf_amt
        data.deposit_amt = vm.deposit_amt
        data.top_up_amt = vm.top_up_amt
        data.bal_amt = vm.bal_amt
        data.put()
    
    def delete(self, movement_date):
        mvs = self.fetch(movement_date)
        
        for mv in mvs:
            mv.key.delete()