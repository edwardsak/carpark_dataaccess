from datalayer.dataaccess.customer import CustomerDataAccess
from datalayer.dataaccess.customeraudittrail import CustomerAuditTrailDataAccess
from datalayer.models.models import Customer

class AccountAppService():
    def update(self, vm):
        try:
            self.valiate(vm)
            
            da = CustomerDataAccess()
            da.update(vm)
            
        except Exception as ex:
            audit_da = CustomerAuditTrailDataAccess()
            audit_da.create(vm.code, 'Update Customer', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = CustomerAuditTrailDataAccess()
        audit_da.create(vm.code, 'Update Customer', 'Ok.')
        
    def valiate(self, vm):
        if len(vm.ic) == 0:
            raise Exception('You must enter an IC/PP No.')
        
        if len(vm.name) == 0:
            raise Exception('You must enter a Name.')
        
    def login(self, vm):
        try:
            q = Customer.query(Customer.ic==vm.ic, Customer.pwd==vm.pwd)
            obj = q.get()
                
            if obj is None:
                raise Exception('Invalid ID or Password.')
            
        except Exception as ex:
            audit_da = CustomerAuditTrailDataAccess()
            audit_da.create(vm.ic, 'Customer login', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = CustomerAuditTrailDataAccess()
        audit_da.create(vm.ic, 'Customer login', 'Ok.')
        
    def change_pwd(self, vm):
        try:
            da = CustomerDataAccess()
            da.change_pwd(vm)
            
        except Exception as ex:
            audit_da = CustomerAuditTrailDataAccess()
            audit_da.create(vm.ic, 'Change Customer Password', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = CustomerAuditTrailDataAccess()
        audit_da.create(vm.code, 'Change Customer Password', 'Ok.')