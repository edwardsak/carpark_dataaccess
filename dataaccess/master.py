from datalayer.models.models import Master

from google.appengine.ext import ndb

class MasterDataAccess():
    def get(self, kind):
        q = Master.query(ancestor=self.get_key(kind))
        master = q.get()
        
        if master is None:
            master = Master(parent=self.get_key(kind))
            master.kind = kind
            master.seq = 0
            
        return master
    
    def get_key(self, key):
        """Constructs a Datastore key for a Master entity with kind."""
        return ndb.Key('Master', key)