from datalayer.models.models import Register, Agent
from datalayer.viewmodels.viewmodels import TranViewModel, CustomerViewModel, CarViewModel, TagViewModel
from datalayer.dataaccess.master import MasterDataAccess
from datalayer.dataaccess.tran import TranDataAccess
from datalayer.dataaccess.customer import CustomerDataAccess
from datalayer.dataaccess.car import CarDataAccess
from datalayer.dataaccess.tag import TagDataAccess
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class RegisterDataAccess():
    def fetch(self, agent_code):
        q = Register.query(ancestor=ndb.Key('Agent', agent_code))
        datas = q.fetch()
        return datas
        
    def create(self, vm):
        # get agent
        agent = Agent.query(Agent.code==vm.agent_code).get()
        if agent is None:
            raise Exception('Agent not found.')
        
        vm.agent = agent
        
        # save customer
        customer_vm = CustomerViewModel()
        customer_vm.ic = vm.customer_ic
        customer_vm.name = vm.customer_name
        customer_vm.address = vm.customer_address
        customer_vm.tel = vm.customer_tel
        customer_vm.hp = vm.customer_hp
        customer_vm.email = vm.customer_email
        
        customer_da = CustomerDataAccess()
        vm.customer = customer_da.save_register(customer_vm)
        
        self.__create(vm)
    
    @ndb.transactional(xg=True)
    def __create(self, vm):
        # save car
        car_vm = CarViewModel()
        car_vm.reg_no = vm.car_reg_no
        car_vm.customer_ic = vm.customer_ic
        car_vm.customer = vm.customer
        car_vm.bal_amt = vm.sub_total
        
        car_da = CarDataAccess()
        vm.car = car_da.save_register(car_vm)
        
        # save tag
        tag_vm = TagViewModel()
        tag_vm.code = vm.tag_code
        tag_vm.agent_code = vm.agent_code
        tag_vm.agent = vm.agent
        tag_vm.car_reg_no = vm.car_reg_no
        tag_vm.car = vm.car
        
        tag_da = TagDataAccess()
        vm.tag = tag_da.demo_save_register(tag_vm)
        
        # get master seq
        master_da = MasterDataAccess()
        master = master_da.get('Register')
        master.seq += 1
        master.put()
        
        # insert register
        tran_code = Register.get_tran_code(master.seq)
        
        data = Register(parent=ndb.Key('Agent', vm.agent_code), id=tran_code)
        data.tran_code = tran_code
        data.tran_type = vm.tran_type
        data.tran_date = vm.tran_date
        data.seq = master.seq
        data.agent_code = vm.agent_code
        data.agent = vm.agent.key
        data.remark = vm.remark
        
        data.car_reg_no = vm.car_reg_no
        data.car = vm.car.key
        
        data.customer_ic = vm.customer_ic
        data.customer_name = vm.customer_name
        data.customer_address = vm.customer_address
        data.customer_tel = vm.customer_tel
        data.customer_hp = vm.customer_hp
        data.customer_email = vm.customer_email
        data.customer = vm.customer.key
        
        data.tag_code = vm.tag_code
        data.tag = vm.tag.key
        
        data.sub_total = vm.sub_total
        
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
        tran_obj.car_reg_no = data.car_reg_no
        
        tran_da = TranDataAccess()
        tran_da.create(tran_obj)