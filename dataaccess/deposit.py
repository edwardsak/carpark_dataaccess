from datalayer.models.models import Deposit, Agent
from datalayer.viewmodels.viewmodels import TranViewModel
from datalayer.dataaccess.basetran import BaseTranDataAccess
from datalayer.dataaccess.master import MasterDataAccess
from datalayer.dataaccess.tran import TranDataAccess
from datalayer.dataaccess.agent import AgentDataAccess
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class DepositDataAccess(BaseTranDataAccess):
    def get_key(self, tran_date, agent_code=None, tran_code=None):
        return self._BaseTranDataAccess__get_key(
                            Deposit, tran_date,
                            Agent, agent_code, 
                            tran_code
                            )
        
    def get(self, tran_date, agent_code, tran_code):
        key = self.get_key(tran_date, agent_code, tran_code)
        return Deposit.query(ancestor=key).get()
    
    def fetch(self, tran_date, agent_code=None, tran_code=None):
        key = self.get_key(tran_date, agent_code, tran_code)
        return Deposit.query(ancestor=key).fetch()
        
    def create(self, vm):
        # get agent
        agent_da = AgentDataAccess()
        agent = agent_da.get(vm.agent_code)
        if agent is None:
            raise Exception('Agent not found.')
        
        vm.agent = agent
        
        self.__create(vm)
    
    @ndb.transactional(xg=True)
    def __create(self, vm):
        # get master seq
        master_da = MasterDataAccess()
        master = master_da.get('Deposit')
        master.seq += 1
        master.put()
        
        # insert deposit
        tran_code = Deposit.get_tran_code(master.seq)
        vm.tran_code = tran_code
        
        data = Deposit(
                       parent=self.get_key(vm.tran_date, vm.agent_code), 
                       id=tran_code
                       )
        data.tran_code = tran_code
        data.tran_type = vm.tran_type
        data.tran_date = vm.tran_date
        data.seq = master.seq
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
        data.last_modified = str(data.created_date)
        data.put()
        
        # insert tran
        tran_obj = TranViewModel()
        tran_obj.tran_code = data.tran_code
        tran_obj.tran_date = data.tran_date
        tran_obj.tran_type = data.tran_type
        tran_obj.agent_code = data.agent_code
        
        tran_da = TranDataAccess()
        tran_da.create(tran_obj)
        
        # update agent bal amt
        agent_da = AgentDataAccess()
        agent = agent_da.get(vm.agent_code)
        agent.bal_amt += vm.amt
        agent.bal_amt = round(agent.bal_amt, 2)
        agent.put()
        
    def verify(self, vm):
        self.__verify(vm)

    @ndb.transactional(xg=True)        
    def __verify(self, vm):
        # get deposit
        pass