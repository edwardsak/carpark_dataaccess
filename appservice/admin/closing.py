from datalayer.models.models import Agent, Car, Register, Deposit, TopUp, Charge, AgentMovement, CarMovement
from datalayer.viewmodels.viewmodels import AgentMovementViewModel, CarMovementViewModel
from datalayer.dataaccess.closing import ClosingDataAccess
from datalayer.dataaccess.agentmovement import AgentMovementDataAccess
from datalayer.dataaccess.carmovement import CarMovementDataAccess
from datalayer.dataaccess.useraudittrail import UserAuditTrailDataAccess
from datalayer.dataaccess.deposit import DepositDataAccess
from datalayer.dataaccess.topup import TopUpDataAccess
from datalayer.dataaccess.register import RegisterDataAccess
from datalayer.dataaccess.charge import ChargeDataAccess

from datetime import timedelta

class ClosingAppService():
    def create(self, vm):
        try:
            da = ClosingDataAccess()
            da.create(vm)
            
        except Exception, ex:
            raise ex
        
    def lock(self, closing_obj):
        try:
            closing_da = ClosingDataAccess()
            closing_da.lock()
            
        except Exception as ex:
            da = UserAuditTrailDataAccess()
            da.create(closing_obj.user_code, 'Lock', 'Fail. Error=%s' % str(ex))
            raise ex
        
        da = UserAuditTrailDataAccess()
        da.create(closing_obj.user_code, 'Lock', 'Ok.')
        
    def unlock(self, closing_obj):
        try:
            closing_da = ClosingDataAccess()
            closing_da.unlock()
            
        except Exception as ex:
            da = UserAuditTrailDataAccess()
            da.create(closing_obj.user_code, 'Unlock', 'Fail. Error=%s' % str(ex))
            raise ex
        
        da = UserAuditTrailDataAccess()
        da.create(closing_obj.user_code, 'Unlock', 'Ok.')
        
    def close(self, closing_obj):
        try:
            # get current closing date
            closing_da = ClosingDataAccess()
            closing = closing_da.get()
            
            # verify is locked
            if closing.audit_lock == False:
                raise Exception('You must lock the system before close.')
            
            # close agent movement
            self.__close_agent_movement(closing.closing_date)
            
            # close car movement
            self.__close_car_movement(closing.closing_date)
            
            # closing
            closing_da.close()
            
        except Exception as ex:
            da = UserAuditTrailDataAccess()
            da.create(closing_obj.user_code, 'Closing', 'Fail. Error=%s' % str(ex))
            raise ex
        
        da = UserAuditTrailDataAccess()
        da.create(closing_obj.user_code, 'Closing', 'Ok.')
    
    # --------------------------------------------------
    def __close_agent_movement(self, closing_date):
        # sum deposit by agent
        deposit_agents = self.__sum_agent_deposit(closing_date)
        
        # sum top_up by agent
        top_up_agents = self.__sum_agent_top_up(closing_date)
        
        # get bf amt
        mv_da = AgentMovementDataAccess()
        movement_date = closing_date + timedelta(days=-1)
        bfs = mv_da.fetch(movement_date)
        
        # group bf by agent code
        bf_agents = {}
        for bf in bfs:
            bf_obj = {}
            bf_obj['agent_code'] = bf.agent_code
            bf_obj['bal_amt'] = bf.bal_amt
            bf_agents[bf.agent_code] = bf_obj
             
        # get agents
        q_agent = Agent.query()
        agents = q_agent.fetch()
        
        # sum to balance
        bals = {}
        for agent in agents:
            bal_obj = None
            if bals.has_key(agent.code):
                bal_obj = bals[agent.code]
            else:
                bal_obj = AgentMovementViewModel()
                bal_obj.agent_code = agent.code
                bal_obj.movement_date = closing_date
                bals[agent.code] = bal_obj
            
            # bf amt
            if bf_agents.has_key(agent.code):
                bf_obj = bf_agents[agent.code]
                bal_obj.bf_amt = bf_obj['bal_amt']    
            
            # deposit amt
            if deposit_agents.has_key(agent.code):
                deposit_obj = deposit_agents[agent.code]
                bal_obj.deposit_amt = deposit_obj['amt']
                
            # top up amt
            if top_up_agents.has_key(agent.code):
                top_up_obj = top_up_agents[agent.code]
                bal_obj.top_up_amt = top_up_obj['amt']
                
        # cal bal amt
        for agent_code in bals:
            bal_obj = bals[agent_code]
            bal_obj.cal_bal_amt()
                
        # delete balance
        mv_da.delete(closing_date)
            
        # insert balance
        for agent_code in bals:
            bal_obj = bals[agent_code]
            mv_da.create(bal_obj)
    
    def __sum_agent_deposit(self, closing_date):
        # get deposit
        da = DepositDataAccess()
        key = da.get_key(closing_date)
        
        q2 = Deposit.query(ancestor=key)
        q2 = q2.filter(Deposit.void==False)
        deposits = q2.fetch()
        
        # sum by agent
        deposit_agents = {}
        for deposit in deposits:
            deposit_obj = None
            if deposit_agents.has_key(deposit.agent_code):
                deposit_obj = deposit_agents[deposit.agent_code]
            else:
                deposit_obj = {}
                deposit_obj['agent_code'] = deposit.agent_code
                deposit_obj['tran_date'] = deposit.tran_date
                deposit_obj['amt'] = 0
                deposit_agents[deposit.agent_code] = deposit_obj
                
            deposit_obj['amt'] += deposit.amt
            
        return deposit_agents
    
    def __sum_agent_top_up(self, closing_date):
        # get topup
        da = TopUpDataAccess()
        key = da.get_key(closing_date)
        
        q2 = TopUp.query(ancestor=key)
        q2 = q2.filter(TopUp.void==False)
        top_ups = q2.fetch()
        
        # sum by agent
        top_up_agents = {}
        for top_up in top_ups:
            top_up_obj = None
            if top_up_agents.has_key(top_up.agent_code):
                top_up_obj = top_up_agents[top_up.agent_code]
            else:
                top_up_obj = {}
                top_up_obj['agent_code'] = top_up.agent_code
                top_up_obj['tran_date'] = top_up.tran_date
                top_up_obj['amt'] = 0
                top_up_agents[top_up.agent_code] = top_up_obj
                
            top_up_obj['amt'] += top_up.amt
            
        return top_up_agents
    
    # --------------------------------------------------
    def __close_car_movement(self, closing_date):
        # sum register by car
        register_cars = self.__sum_car_register(closing_date)
        
        # sum top_up by car
        top_up_cars = self.__sum_car_top_up(closing_date)
        
        # sum charge by car
        charge_cars = self.__sum_car_charge(closing_date)
        
        # get bf amt
        mv_da = CarMovementDataAccess()
        movement_date = closing_date + timedelta(days=-1)
        bfs = mv_da.fetch(movement_date)
        
        # group bf by car
        bf_cars = {}
        for bf in bfs:
            bf_obj = {}
            bf_obj['car_reg_no'] = bf.car_reg_no
            bf_obj['bal_amt'] = bf.bal_amt
            bf_cars[bf.car_reg_no] = bf_obj
             
        # get cars
        q_car = Car.query()
        cars = q_car.fetch()
        
        # sum to balance
        bals = {}
        for car in cars:
            bal_obj = None
            if bals.has_key(car.reg_no):
                bal_obj = bals[car.reg_no]
            else:
                bal_obj = CarMovementViewModel()
                bal_obj.car_reg_no = car.reg_no
                bal_obj.movement_date = closing_date
                bals[car.reg_no] = bal_obj
            
            # bf amt
            if bf_cars.has_key(car.reg_no):
                bf_obj = bf_cars[car.reg_no]
                bal_obj.bf_amt = bf_obj['bal_amt']    
            
            # register amt
            if register_cars.has_key(car.reg_no):
                register_obj = register_cars[car.reg_no]
                bal_obj.register_amt = register_obj['amt']
                
            # top up amt
            if top_up_cars.has_key(car.reg_no):
                top_up_obj = top_up_cars[car.reg_no]
                bal_obj.top_up_amt = top_up_obj['amt']
                
            # charge amt
            if charge_cars.has_key(car.reg_no):
                charge_obj = charge_cars[car.reg_no]
                bal_obj.charge_amt = charge_obj['amt']
                
        # cal bal amt
        for car_reg_no in bals:
            bal_obj = bals[car_reg_no]
            bal_obj.cal_bal_amt()
                
        # delete balance
        mv_da.delete(closing_date)
            
        # insert balance
        for car_reg_no in bals:
            bal_obj = bals[car_reg_no]
            mv_da.create(bal_obj)
            
    def __sum_car_register(self, closing_date):
        # get register
        da = RegisterDataAccess()
        key = da.get_key(closing_date)
        
        q2 = Register.query(ancestor=key)
        q2 = q2.filter(Register.void==False)
        registers = q2.fetch()
        
        # sum by car
        register_cars = {}
        for register in registers:
            register_obj = None
            if register_cars.has_key(register.car_reg_no):
                register_obj = register_cars[register.car_reg_no]
            else:
                register_obj = {}
                register_obj['car_reg_no'] = register.car_reg_no
                register_obj['tran_date'] = register.tran_date
                register_obj['amt'] = 0
                register_cars[register.car_reg_no] = register_obj
                
            register_obj['amt'] += register.sub_total
            
        return register_cars
    
    def __sum_car_top_up(self, closing_date):
        # get topup
        da = TopUpDataAccess()
        key = da.get_key(closing_date)
        
        q2 = TopUp.query(ancestor=key)
        q2 = q2.filter(TopUp.void==False)
        top_ups = q2.fetch()
        
        # sum by car
        top_up_cars = {}
        for top_up in top_ups:
            top_up_obj = None
            if top_up_cars.has_key(top_up.car_reg_no):
                top_up_obj = top_up_cars[top_up.car_reg_no]
            else:
                top_up_obj = {}
                top_up_obj['car_reg_no'] = top_up.car_reg_no
                top_up_obj['tran_date'] = top_up.tran_date
                top_up_obj['amt'] = 0
                top_up_cars[top_up.car_reg_no] = top_up_obj
                
            top_up_obj['amt'] += top_up.sub_total
            
        return top_up_cars
    
    def __sum_car_charge(self, closing_date):
        # get charge
        da = ChargeDataAccess()
        key = da.get_key(closing_date)
        
        q2 = Charge.query(ancestor=key)
        q2 = q2.filter(Charge.void==False)
        charges = q2.fetch()
        
        # sum by car
        charge_cars = {}
        for charge in charges:
            charge_obj = None
            if charge_cars.has_key(charge.car_reg_no):
                charge_obj = charge_cars[charge.car_reg_no]
            else:
                charge_obj = {}
                charge_obj['car_reg_no'] = charge.car_reg_no
                charge_obj['tran_date'] = charge.tran_date
                charge_obj['amt'] = 0
                charge_cars[charge.car_reg_no] = charge_obj
                
            charge_obj['amt'] += charge.sub_total
            
        return charge_cars
    
    # --------------------------------------------------
    def revert(self, closing_obj):
        try:
            # get closing
            closing_da = ClosingDataAccess()
            closing = closing_da.get()
            
            # verify lock
            if closing.audit_lock == False:
                raise Exception('You must lock the system before revert.')
            
            # delete agent balance
            self.__delete_agent_movement(closing.closing_date)
            
            # delete car balance
            self.__delete_car_movement(closing.closing_date)
            
            # update
            closing_da.revert()
            
        except Exception as ex:
            da = UserAuditTrailDataAccess()
            da.create(closing_obj.user_code, 'Closing', 'Fail. Error=%s' % str(ex))
            raise ex
        
        da = UserAuditTrailDataAccess()
        da.create(closing_obj.user_code, 'Closing', 'Ok.')
        
    def __delete_agent_movement(self, closing_date):
        q = AgentMovement.query(AgentMovement.movement_date >= closing_date + timedelta(days=-1))
        q = q.filter(AgentMovement.movement_date <= closing_date)
        bals = q.fetch()
            
        for bal in bals:
            bal.key.delete()
            
    def __delete_car_movement(self, closing_date):
        q = CarMovement.query(CarMovement.movement_date >= closing_date + timedelta(days=-1))
        q = q.filter(CarMovement.movement_date <= closing_date)
        bals = q.fetch()
            
        for bal in bals:
            bal.key.delete()