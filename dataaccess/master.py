from datalayer.models.models import Master

from google.appengine.ext import ndb

class MasterDataAccess():
    def get(self, kind):
        q = Master.query(ancestor=ndb.Key('Master', kind))
        master = q.get()
        
        if master is None:
            master = Master(parent=ndb.Key('Master', kind), id=kind)
            master.kind = kind
            master.seq = 0
            
        return master