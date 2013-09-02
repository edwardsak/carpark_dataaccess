from datalayer.dataaccess.agent import AgentDataAccess
from datalayer.dataaccess.agentaudittrail import AgentAuditTrailDataAccess
from datalayer.models.models import Agent

class AgentAppService():
    def update(self, vm):
        try:
            self.valiate(vm)
            
            da = AgentDataAccess()
            da.update(vm)
            
        except Exception as ex:
            # audit trail, fail
            audit_da = AgentAuditTrailDataAccess()
            audit_da.create(vm.agent_code, 'Update Agent', 'Fail. Error=%s' % str(ex))
            
            raise ex
        
        # audit trail, ok
        audit_da = AgentAuditTrailDataAccess()
        audit_da.create(vm.agent_code, 'Update Agent', 'Ok.')
        
    def valiate(self, vm):
        if len(vm.code) == 0:
            raise Exception('You must enter an Agent ID.')
        
        if len(vm.name) == 0:
            raise Exception('You must enter a Name.')
        
    def login(self, vm):
        q = Agent.query(Agent.code==vm.code, Agent.pwd==vm.pwd)
        obj = q.get()
            
        if obj is None:
            raise Exception('Invalid ID or Password.')
        
    def reset_pwd(self, vm):
        try:
            da = AgentDataAccess()
            da.reset_pwd(vm)
            
        except Exception as ex:
            # audit trail, fail
            audit_da = AgentAuditTrailDataAccess()
            audit_da.create(vm.agent_code, 'Reset Agent Password', 'Fail. Error=%s' % str(ex))
            
            raise ex
        
        # audit trail, ok
        audit_da = AgentAuditTrailDataAccess()
        audit_da.create(vm.agent_code, 'Reset Agent Password', 'Ok.')
        
    def change_pwd(self, vm):
        try:
            da = AgentDataAccess()
            da.change_pwd(vm)
            
        except Exception as ex:
            # audit trail, fail
            audit_da = AgentAuditTrailDataAccess()
            audit_da.create(vm.agent_code, 'Change Agent Password', 'Fail. Error=%s' % str(ex))
            
            raise ex
        
        # audit trail, ok
        audit_da = AgentAuditTrailDataAccess()
        audit_da.create(vm.agent_code, 'Change Agent Password', 'Ok.')