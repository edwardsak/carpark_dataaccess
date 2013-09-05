from datalayer.dataaccess.closing import ClosingDataAccess

class ClosingAppService():
    def create(self, vm):
        try:
            da = ClosingDataAccess()
            da.create(vm)
            
        except Exception, ex:
            raise ex