from datalayer.models.models import Tran

from google.appengine.ext import ndb

class TranDataAccess():
    @staticmethod
    def get_ndb_key(tran_date):
        return "%s" % (tran_date.strftime('%Y%m%d'))
    
    def get(self, tran_date):
        key = TranDataAccess.get_ndb_key(tran_date)
        q = Tran.query(ancestor=ndb.Key('Tran', key))
        return q.fetch()
        
    def create(self, tran_obj):
        # get last tran seq of that day
        key = TranDataAccess.get_ndb_key(tran_obj.tran_date)
        last_tran = Tran.query(ancestor=ndb.Key('Tran', key)).order(-Tran.seq).get()
        
        seq = 0
        if last_tran:
            seq = last_tran.seq
            seq += 1
            
        tran = Tran(parent=ndb.Key('Tran', key), id=tran_obj.tran_code)
        tran.tran_type = tran_obj.tran_type
        tran.tran_code = tran_obj.tran_code
        tran.tran_date = tran_obj.tran_date
        tran.seq = seq
        tran.agent_code = tran_obj.agent_code
        tran.car_reg_no = tran_obj.car_reg_no
        tran.put()