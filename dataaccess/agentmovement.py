from datalayer.models.models import AgentMovement

from google.appengine.ext import ndb

class AgentMovementDataAccess():
    def get_key(self, key):
        return ndb.Key('AgentMovement', key)
    
    def create(self, vm):
        data = AgentMovement()
        data.agent_id = vm.agent_code
        data.movement_date = vm.movement_date
        data.bf_amt = vm.bf_amt
        data.deposit_amt = vm.deposit_amt
        data.top_up_amt = vm.top_up_amt
        data.bal_amt = vm.bal_amt
        data.put()
    
    def delete(self, mv_date):
        q = AgentMovement.query(AgentMovement.movement_date == mv_date)
        mvs = q.fetch()
        
        for mv in mvs:
            mv.key.delete()