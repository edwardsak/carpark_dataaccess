from datalayer.models.models import TopUp
from datalayer.viewmodels.viewmodels import TranViewModel
from datalayer.dataaccess.master import MasterDataAccess
from datalayer.dataaccess.tran import TranDataAccess
from datalayer.dataaccess.agent import AgentDataAccess
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class TopUpDataAccess():
    def get_key(self, key):
        return ndb.Key('TopUp', key)
    
    def get(self, agent_code):
        q = TopUp.query(ancestor=self.get_key(agent_code))
        datas = q.fetch()
        return datas
        
    def create(self, vm):
        self.__create(vm)
    
    @ndb.transactional(xg=True)
    def __create(self, vm):
        # get master seq
        master_da = MasterDataAccess()
        master = master_da.get('TopUp')
        master.seq += 1
        master.put()
        
        # insert deposit
        data = TopUp(parent=self.get_key(vm.agent_code))
        data.tran_date = vm.tran_date
        data.seq = master.seq
        data.tran_code = data.get_tran_code()
        data.agent_code = vm.agent_code
        data.agent = vm.agent.key
        data.remark = vm.remark
        
        data.car_reg_no = vm.car_reg_no
        data.sub_total = vm.sub_total
        data.comm_per = vm.comm_per
        data.comm_amt = vm.comm_amt
        data.amt = vm.amt
        
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
        agent.bal_amt -= vm.amt
        agent.bal_amt = round(agent.bal_amt, 2)
        
        if agent.bal_amt < 0:
            raise Exception('You have no more Balance.')
        
        agent.put()