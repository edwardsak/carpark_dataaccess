from datalayer.models.models import Deposit
from datalayer.viewmodels.viewmodels import TranViewModel
from datalayer.dataaccess.master import MasterDataAccess
from datalayer.dataaccess.tran import TranDataAccess
from datalayer.dataaccess.agent import AgentDataAccess
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class DepositDataAccess():
    def get_key(self, key):
        return ndb.Key('Deposit', key)
    
    def get(self, agent_code):
        q = Deposit.query(ancestor=self.get_key(agent_code))
        datas = q.fetch()
        return datas
        
    def create(self, vm):
        self.__create(vm)
    
    @ndb.transactional(xg=True)
    def __create(self, vm):
        # get master seq
        master_da = MasterDataAccess()
        master = master_da.get('Deposit')
        master.seq += 1
        master.put()
        
        # insert deposit
        data = Deposit(parent=self.get_key(vm.agent_code))
        data.tran_date = vm.tran_date
        data.seq = master.seq
        data.tran_code = data.get_tran_code()
        data.agent_code = vm.agent_code
        data.agent = vm.agent.key
        data.remark = vm.remark
        
        data.amt = vm.amt
        
        data.payment_date = vm.payment_date
        data.payment_type = vm.payment_type
        data.payment_ref_no = vm.payment_ref_no
        data.payment_file_name = vm.payment_file_name
        data.payment_url = vm.payment_url
        
        data.verified_by = ''
        data.verified_date = None
        data.verify_status = 0
        
        data.created_by = vm.user_code
        data.created_date = DateTime.malaysia_now()
        data.modified_by = ''
        data.modified_date = None
        data.void_by = ''
        data.void_date = None
        data.void = False
        data.last_modified = str(data.create_date)
        data.put()
        
        # insert tran
        tran_obj = TranViewModel()
        tran_obj.tran_code = data.tran_code
        tran_obj.tran_date = data.tran_date
        tran_obj.tran_type = data.tran_type
        
        tran_da = TranDataAccess()
        tran_da.create(tran_obj)
        
        # update agent bal amt
        agent_da = AgentDataAccess()
        agent = agent_da.get(vm.agent_code)
        agent.bal_amt += vm.amt
        agent.bal_amt = round(agent.bal_amt, 2)
        agent.put()