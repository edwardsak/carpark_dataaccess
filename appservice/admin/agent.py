from datalayer.dataaccess.agent import AgentDataAccess
from datalayer.dataaccess.useraudittrail import UserAuditTrailDataAccess

class AgentAppService():
    def create(self, vm):
        try:
            self.validate_code(vm)
            self.validate_name(vm)
            
            if vm.pwd == None or len(vm.pwd) < 1:
                raise Exception("You must enter a Password.")
            
            self.validate_account_type(vm)
            self.validate_comm_per(vm)
            
            # init data
            vm.bal_amt = 0
            
            da = AgentDataAccess()
            da.create(vm)
            
        except Exception as ex:
            audit_da = UserAuditTrailDataAccess()
            audit_da.create(vm.user_code, 'Create Agent', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = UserAuditTrailDataAccess()
        audit_da.create(vm.user_code, 'Create Agent', 'Ok.')
        
    def update(self, vm):
        try:
            self.validate_code(vm)
            self.validate_name(vm)
            self.validate_account_type(vm)
            self.validate_comm_per(vm)
            
            da = AgentDataAccess()
            da.update(vm)
            
        except Exception as ex:
            audit_da = UserAuditTrailDataAccess()
            audit_da.create(vm.user_code, 'Update Agent', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = UserAuditTrailDataAccess()
        audit_da.create(vm.user_code, 'Update Agent', 'Ok.')
        
    def validate_code(self, vm):
        if vm.code == None or len(vm.code) < 1:
            raise Exception("You must enter an Agent ID.")
        
    def validate_name(self, vm):
        if vm.name == None or len(vm.name) < 1:
            raise Exception("You must enter an Agent Name.")
        
    def validate_account_type(self, vm):
        if vm.account_type < 1 or vm.account_type > 2:
            raise Exception("You must enter a valid Account Type.")
        
    def validate_comm_per(self, vm):
        if vm.comm_per < 0:
            raise Exception("You must enter a valid Comm. %.")