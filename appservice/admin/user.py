from datalayer.dataaccess.user import UserDataAccess
from datalayer.dataaccess.useraudittrail import UserAuditTrailDataAccess

class UserAppService():
    def create(self, vm):
        try:
            self.validate_code(vm)
            self.validate_name(vm)
            
            if vm.pwd == None or len(vm.pwd) < 1:
                raise Exception("You must enter a Password.")
            
            self.validate_level(vm)
            
            da = UserDataAccess()
            da.create(vm)
            
        except Exception as ex:
            audit_da = UserAuditTrailDataAccess()
            audit_da.create(vm.user_code, 'Create User', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = UserAuditTrailDataAccess()
        audit_da.create(vm.user_code, 'Create User', 'Ok.')
        
    def update(self, vm):
        try:
            self.validate_code(vm)
            self.validate_name(vm)
            self.validate_level(vm)
            
            da = UserDataAccess()
            da.update(vm)
            
        except Exception as ex:
            audit_da = UserAuditTrailDataAccess()
            audit_da.create(vm.user_code, 'Update User', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = UserAuditTrailDataAccess()
        audit_da.create(vm.user_code, 'Update User', 'Ok.')
        
    def validate_code(self, vm):
        if vm.code == None or len(vm.code) < 1:
            raise Exception("You must enter an User ID.")
        
    def validate_name(self, vm):
        if vm.name == None or len(vm.name) < 1:
            raise Exception("You must enter an User Name.")
        
    def validate_level(self, vm):
        if vm.account_type < 1 or vm.account_type > 5:
            raise Exception("You must enter a valid Level.")