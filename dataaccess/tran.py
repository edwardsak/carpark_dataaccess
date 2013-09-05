from datalayer.models.models import Tran

from google.appengine.ext import ndb

class TranDataAccess():
    @staticmethod
    def get_ndb_key(tran_date):
        return "%s" % (tran_date.strftime('%Y%m%d'))
    
    def get_key(self, key):
        return ndb.Key('Tran', key)
    
    def get(self, key):
        q = Tran.query(ancestor=self.get_key(key))
        return q.fetch()
        
    def create(self, tran_obj):
        # get last tran seq of that day
        key = TranDataAccess.get_ndb_key(tran_obj.tran_date)
        last_tran = Tran.query(ancestor=self.get_key(key)).order(-Tran.seq).get()
        
        seq = 0
        if last_tran:
            seq = last_tran.seq
            seq += 1
            
        tran = Tran(parent=self.get_key(key))
        tran.tran_type = tran_obj.tran_type
        tran.tran_id = tran_obj.tran_id
        tran.tran_date = tran_obj.tran_date
        tran.seq = seq
        tran.put()