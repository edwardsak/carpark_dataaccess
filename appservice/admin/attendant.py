from datalayer.dataaccess.attendant import AttendantDataAccess
from datalayer.dataaccess.useraudittrail import UserAuditTrailDataAccess

class AttendantAppService():
    def create(self, vm):
        try:
            self.validate_code(vm)
            self.validate_name(vm)
            
            if vm.pwd == None or len(vm.pwd) < 1:
                raise Exception("You must enter a Password.")
            
            self.validate_comm_per(vm)
            
            da = AttendantDataAccess()
            da.create(vm)
            
        except Exception as ex:
            audit_da = UserAuditTrailDataAccess()
            audit_da.create(vm.user_code, 'Create Attendant', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = UserAuditTrailDataAccess()
        audit_da.create(vm.user_code, 'Create Attendant', 'Ok.')
        
    def update(self, vm):
        try:
            self.validate_code(vm)
            self.validate_name(vm)
            self.validate_comm_per(vm)
            
            da = AttendantDataAccess()
            da.update(vm)
            
        except Exception as ex:
            audit_da = UserAuditTrailDataAccess()
            audit_da.create(vm.user_code, 'Update Attendant', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = UserAuditTrailDataAccess()
        audit_da.create(vm.user_code, 'Update Attendant', 'Ok.')
        
    def validate_code(self, vm):
        if vm.code == None or len(vm.code) < 1:
            raise Exception("You must enter an Attendant ID.")
        
    def validate_name(self, vm):
        if vm.name == None or len(vm.name) < 1:
            raise Exception("You must enter an Attendant Name.")
        
    def validate_comm_per(self, vm):
        if vm.comm_per < 0:
            raise Exception("You must enter a valid Comm. %.")