from datalayer.models.models import Buy, Agent
from datalayer.viewmodels.viewmodels import TranViewModel
from datalayer.dataaccess.master import MasterDataAccess
from datalayer.dataaccess.tran import TranDataAccess
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class BuyDataAccess():
    def fetch(self, agent_code):
        q = Buy.query(ancestor=ndb.Key('Agent', agent_code))
        buys = q.fetch()
        return buys
        
    def create(self, buy_obj):
        # get agent
        agent = Agent.query(Agent.code==buy_obj.agent_code).get()
        if agent is None:
            raise Exception('Agent not found.')
        
        buy_obj.agent = agent
        
        self.__create(buy_obj)
    
    @ndb.transactional(xg=True)
    def __create(self, buy_obj):
        # get master seq
        master_da = MasterDataAccess()
        master = master_da.get('Buy')
        master.seq += 1
        master.put()
        
        # insert buy
        tran_code = Buy.get_tran_code(master.seq)
        
        buy = Buy(parent=ndb.Key('Agent', buy_obj.agent_code), id=tran_code)
        buy.tran_code = tran_code
        buy.tran_type = buy_obj.tran_type
        buy.tran_date = buy_obj.tran_date
        buy.seq = master.seq
        buy.agent_code = buy_obj.agent_code
        buy.agent = buy_obj.agent.key
        buy.remark = buy_obj.remark
        
        buy.qty = buy_obj.qty
        buy.unit_price = buy_obj.unit_price
        buy.sub_total = buy_obj.sub_total
        buy.comm_per = buy_obj.comm_per
        buy.comm_amt = buy_obj.comm_amt
        buy.amt = buy_obj.amt
        
        buy.payment_date = buy_obj.payment_date
        buy.payment_type = buy_obj.payment_type
        buy.payment_ref_no = buy_obj.payment_ref_no
        
        buy.verified_by = ''
        buy.verified_date = None
        buy.verify_status = 0
        
        buy.created_by = buy_obj.user_code
        buy.created_date = DateTime.malaysia_now()
        buy.modified_by = ''
        buy.modified_date = None
        buy.void_by = ''
        buy.void_date = None
        buy.void = False
        buy.last_modified = str(buy.created_date)
        buy.put()
        
        # insert tran
        tran_obj = TranViewModel()
        tran_obj.tran_code = buy.tran_code
        tran_obj.tran_date = buy.tran_date
        tran_obj.tran_type = buy.tran_type
        tran_obj.agent_code = buy.agent_code
        
        tran_da = TranDataAccess()
        tran_da.create(tran_obj)