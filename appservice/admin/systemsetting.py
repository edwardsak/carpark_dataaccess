from datalayer.dataaccess.systemsetting import SystemSettingDataAccess
from sharelib.object import Object

class SystemSettingAppService():
    def create(self, vm):
        try:
            da = SystemSettingDataAccess()
            da.create(vm)
            
        except Exception, ex:
            raise ex