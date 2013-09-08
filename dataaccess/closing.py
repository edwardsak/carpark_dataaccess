from datalayer.models.models import Closing

from datetime import timedelta

from google.appengine.ext import ndb

class ClosingDataAccess():
    def create(self, closing_obj):
        self.__create(closing_obj)
    
    @ndb.transactional(xg=True)
    def __create(self, closing_obj):
        closing = Closing()
        closing.closing_date = closing_obj.closing_date
        closing.audit_lock = False
        closing.put()
        
    def lock(self):
        q = Closing.query()
        closing = q.get()
            
        closing.audit_lock = True
        closing.put()
        
    def unlock(self):
        q = Closing.query()
        closing = q.get()
            
        closing.audit_lock = False
        closing.put()
        
    def close(self):
        q = Closing.query()
        closing = q.get()
        
        closing.closing_date = closing.closing_date + timedelta(days=1)
        closing.audit_lock = False
        closing.put()
        
    def revert(self):
        q = Closing.query()
        closing = q.get()
        
        closing.closing_date = closing.closing_date + timedelta(days=-1)
        closing.audit_lock = False
        closing.put()