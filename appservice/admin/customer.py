from datalayer.dataaccess.customer import CustomerDataAccess
from datalayer.dataaccess.useraudittrail import UserAuditTrailDataAccess

class CustomerAppService():
    def create(self, vm):
        try:
            self.validate_ic(vm)
            self.validate_name(vm)
            
            da = CustomerDataAccess()
            da.create(vm)
            
        except Exception as ex:
            audit_da = UserAuditTrailDataAccess()
            audit_da.create(vm.user_code, 'Create Customer', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = UserAuditTrailDataAccess()
        audit_da.create(vm.user_code, 'Create Customer', 'Ok.')
        
    def update(self, vm):
        try:
            self.validate_ic(vm)
            
            da = CustomerDataAccess()
            da.update(vm)
            
        except Exception as ex:
            audit_da = UserAuditTrailDataAccess()
            audit_da.create(vm.user_code, 'Update Customer', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = UserAuditTrailDataAccess()
        audit_da.create(vm.user_code, 'Update Customer', 'Ok.')
        
    def validate_ic(self, vm):
        if vm.ic == None or len(vm.ic) < 1:
            raise Exception("You must enter an IC/PP No.")
        
    def validate_name(self, vm):
        if vm.name == None or len(vm.name) < 1:
            raise Exception("You must enter a Customer Name.")