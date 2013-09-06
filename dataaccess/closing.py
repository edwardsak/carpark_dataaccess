from datalayer.models.models import Closing

from google.appengine.ext import ndb

class ClosingDataAccess():
    def create(self, vm):
        self.__create(vm)
    
    @ndb.transactional(xg=True)
    def __create(self, vm):
        data = Closing()
        data.closing_date = vm.closing_date
        data.put()
        
    def update(self, vm):
        data = Closing.query().get()
        data.closing_date = vm.closing_date
        data.put()