from datalayer.models.models import TopUp, Agent, Car
from datalayer.viewmodels.viewmodels import TranViewModel
from datalayer.dataaccess.master import MasterDataAccess
from datalayer.dataaccess.tran import TranDataAccess
from datalayer.dataaccess.agent import AgentDataAccess
from datalayer.dataaccess.car import CarDataAccess
from sharelib.utils import DateTime

from google.appengine.ext import ndb

class TopUpDataAccess():
    def fetch(self, agent_code):
        q = TopUp.query(ancestor=ndb.Key('Agent', agent_code))
        datas = q.fetch()
        return datas
        
    def create(self, vm):
        # get agent
        agent = Agent.query(Agent.code==vm.agent_code).get()
        if agent is None:
            raise Exception('Agent not found.')
        
        vm.agent = agent
        
        # get car
        car = Car.query(Car.reg_no==vm.car_reg_no).get()
        if car is None:
            raise Exception('Car not found.')
        
        vm.car = car
        
        self.__create(vm)
    
    @ndb.transactional(xg=True)
    def __create(self, vm):
        # get master seq
        master_da = MasterDataAccess()
        master = master_da.get('TopUp')
        master.seq += 1
        master.put()
        
        # insert deposit
        tran_code = TopUp.get_tran_code(master.seq)
        
        data = TopUp(parent=ndb.Key('Agent', vm.agent_code), id=tran_code)
        data.tran_code = tran_code
        data.tran_type = vm.tran_type
        data.tran_date = vm.tran_date
        data.seq = master.seq
        data.agent_code = vm.agent_code
        data.agent = vm.agent.key
        data.remark = vm.remark
        
        data.car_reg_no = vm.car_reg_no
        data.car = vm.car.key
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
        
        # update agent bal amt
        agent_da = AgentDataAccess()
        agent = agent_da.get(vm.agent_code)
        agent.bal_amt -= vm.amt
        agent.bal_amt = round(agent.bal_amt, 2)
        
        if agent.bal_amt < 0:
            raise Exception('You have no more Balance.')
        
        agent.put()
        
        # update car bal amt
        car_da = CarDataAccess()
        car = car_da.get(vm.car_reg_no)
        car.bal_amt += vm.sub_total
        car.bal_amt = round(car.bal_amt, 2)
        car.put()