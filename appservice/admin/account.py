from datalayer.models.models import User
from datalayer.dataaccess.user import UserDataAccess
from datalayer.dataaccess.useraudittrail import UserAuditTrailDataAccess

from google.appengine.ext import ndb

class AccountAppService():
    def login(self, vm):
        try:
            q = User.query(ancestor=ndb.Key(User, vm.code))
            q = q.filter(User.pwd==vm.pwd)
            obj = q.get()
                
            if obj is None:
                raise Exception('Invalid ID or Password.')
        
        except Exception as ex:
            audit_da = UserAuditTrailDataAccess()
            audit_da.create(vm.user_code, 'Login', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = UserAuditTrailDataAccess()
        audit_da.create(vm.user_code, 'Login', 'Ok.')
        
    def reset_pwd(self, vm):
        try:
            da = UserDataAccess()
            da.reset_pwd(vm)
        
        except Exception as ex:
            audit_da = UserAuditTrailDataAccess()
            audit_da.create(vm.user_code, 'Reset User Password', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = UserAuditTrailDataAccess()
        audit_da.create(vm.user_code, 'Reset User Password', 'Ok.')
        
    def change_pwd(self, vm):
        try:
            da = UserDataAccess()
            da.change_pwd(vm)
            
        except Exception as ex:
            audit_da = UserAuditTrailDataAccess()
            audit_da.create(vm.user_code, 'Change User Password', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = UserAuditTrailDataAccess()
        audit_da.create(vm.user_code, 'Change User Password', 'Ok.')