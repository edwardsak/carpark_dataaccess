from datalayer.dataaccess.attendant import AttendantDataAccess
from datalayer.dataaccess.attendantaudittrail import AttendantAuditTrailDataAccess
from datalayer.models.models import Attendant

from google.appengine.ext import ndb

class AccountAppService():
    def update(self, vm):
        try:
            self.valiate(vm)
            
            da = AttendantDataAccess()
            da.update(vm)
            
        except Exception as ex:
            # audit trail, fail
            audit_da = AttendantAuditTrailDataAccess()
            audit_da.create(vm.code, 'Update Attendant', 'Fail. Error=%s' % str(ex))
            
            raise ex
        
        # audit trail, ok
        audit_da = AttendantAuditTrailDataAccess()
        audit_da.create(vm.code, 'Update Attendant', 'Ok.')
        
    def valiate(self, vm):
        if len(vm.code) == 0:
            raise Exception('You must enter an Attendant ID.')
        
        if len(vm.name) == 0:
            raise Exception('You must enter a Name.')
        
    def login(self, vm):
        q = Attendant.query(ancestor=ndb.Key(Attendant, vm.code))
        q = q.filter(Attendant.pwd==vm.pwd)
        obj = q.get()
            
        if obj is None:
            raise Exception('Invalid ID or Password.')
        
    def change_pwd(self, vm):
        try:
            da = AttendantDataAccess()
            da.change_pwd(vm)
            
        except Exception as ex:
            # audit trail, fail
            audit_da = AttendantAuditTrailDataAccess()
            audit_da.create(vm.code, 'Change Attendant Password', 'Fail. Error=%s' % str(ex))
            
            raise ex
        
        # audit trail, ok
        audit_da = AttendantAuditTrailDataAccess()
        audit_da.create(vm.code, 'Change Attendant Password', 'Ok.')