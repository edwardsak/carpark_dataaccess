from datalayer.models.models import Register
from datalayer.viewmodels.viewmodels import TranViewModel
from datalayer.dataaccess.master import MasterDataAccess
from datalayer.dataaccess.tran import TranDataAccess
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class RegisterDataAccess():
    def get_key(self, key):
        return ndb.Key('Register', key)
    
    def get(self, agent_code):
        q = Register.query(ancestor=self.get_key(agent_code))
        datas = q.fetch()
        return datas
        
    def create(self, vm):
        self.__create(vm)
    
    @ndb.transactional(xg=True)
    def __create(self, vm):
        # get master seq
        master_da = MasterDataAccess()
        master = master_da.get('Register')
        master.seq += 1
        master.put()
        
        # insert deposit
        data = Register(parent=self.get_key(vm.agent_code))
        data.tran_date = vm.tran_date
        data.seq = master.seq
        data.tran_code = data.get_tran_code()
        data.agent_code = vm.agent_code
        data.agent = vm.agent.key
        data.remark = vm.remark
        
        data.car_reg_no = vm.car_reg_no
        data.tag_no = vm.tag_no
        
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