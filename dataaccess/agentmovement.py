from datalayer.models.models import AgentMovement

from google.appengine.ext import ndb

class AgentMovementDataAccess():
    def create(self, vm):
        movement_code = AgentMovement.get_movement_code(vm.agent_code, vm.movement_date)
        
        data = AgentMovement(parent=ndb.Key('Agent', vm.agent_code), id=movement_code)
        data.movement_code = movement_code
        data.agent_code = vm.agent_code
        data.movement_date = vm.movement_date
        data.bf_amt = vm.bf_amt
        data.deposit_amt = vm.deposit_amt
        data.top_up_amt = vm.top_up_amt
        data.bal_amt = vm.bal_amt
        data.put()
    
    def delete(self, movement_date):
        q = AgentMovement.query(AgentMovement.movement_date==movement_date)
        mvs = q.fetch()
        
        for mv in mvs:
            mv.key.delete()