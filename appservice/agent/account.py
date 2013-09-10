from datalayer.dataaccess.agent import AgentDataAccess
from datalayer.dataaccess.agentaudittrail import AgentAuditTrailDataAccess
from datalayer.models.models import Agent

from google.appengine.ext import ndb

class AccountAppService():
    def update(self, vm):
        try:
            self.valiate(vm)
            
            da = AgentDataAccess()
            da.update(vm)
            
        except Exception as ex:
            audit_da = AgentAuditTrailDataAccess()
            audit_da.create(vm.code, 'Update Agent', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = AgentAuditTrailDataAccess()
        audit_da.create(vm.code, 'Update Agent', 'Ok.')
        
    def valiate(self, vm):
        if len(vm.code) == 0:
            raise Exception('You must enter an Agent ID.')
        
        if len(vm.name) == 0:
            raise Exception('You must enter a Name.')
        
    def login(self, vm):
        try:
            q = Agent.query(ancestor=ndb.Key(Agent, vm.code))
            q = q.filter(Agent.pwd==vm.pwd)
            obj = q.get()
                
            if obj is None:
                raise Exception('Invalid ID or Password.')
            
        except Exception as ex:
            audit_da = AgentAuditTrailDataAccess()
            audit_da.create(vm.code, 'Agent login', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = AgentAuditTrailDataAccess()
        audit_da.create(vm.code, 'Agent login', 'Ok.')
        
    def change_pwd(self, vm):
        try:
            da = AgentDataAccess()
            da.change_pwd(vm)
            
        except Exception as ex:
            audit_da = AgentAuditTrailDataAccess()
            audit_da.create(vm.code, 'Change Agent Password', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = AgentAuditTrailDataAccess()
        audit_da.create(vm.code, 'Change Agent Password', 'Ok.')