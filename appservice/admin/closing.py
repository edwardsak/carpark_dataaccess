from datalayer.models.models import Closing, Agent, Deposit, TopUp, AgentMovement
from datalayer.viewmodels.viewmodels import AgentMovementViewModel
from datalayer.dataaccess.closing import ClosingDataAccess
from datalayer.dataaccess.agentmovement import AgentMovementDataAccess
from datalayer.dataaccess.useraudittrail import UserAuditTrailDataAccess

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
            da.create(closing_obj.user_id, 'Lock', 'Fail. Error=%s' % str(ex))
            raise ex
        
        da = UserAuditTrailDataAccess()
        da.create(closing_obj.user_id, 'Lock', 'Ok.')
        
    def unlock(self, closing_obj):
        try:
            closing_da = ClosingDataAccess()
            closing_da.unlock()
            
        except Exception as ex:
            da = UserAuditTrailDataAccess()
            da.create(closing_obj.user_id, 'Unlock', 'Fail. Error=%s' % str(ex))
            raise ex
        
        da = UserAuditTrailDataAccess()
        da.create(closing_obj.user_id, 'Unlock', 'Ok.')
        
    def close(self, closing_obj):
        try:
            # get current closing date
            q = Closing.query()
            closing = q.get()
            
            # verify is locked
            if closing.audit_lock == False:
                raise Exception('You must lock the system before close.')
            
            # close agent movement
            self.__close_agent_movement(closing.closing_date)
            
            # close car movement
            
            
            # closing
            closing_da = ClosingDataAccess()
            closing_da.close()
            
        except Exception as ex:
            da = UserAuditTrailDataAccess()
            da.create(closing_obj.user_id, 'Closing', 'Fail. Error=%s' % str(ex))
            raise ex
        
        da = UserAuditTrailDataAccess()
        da.create(closing_obj.user_id, 'Closing', 'Ok.')
        
    def __close_agent_movement(self, closing_date):
        # sum deposit by agent
        deposit_agents = self.__sum_agent_deposit(closing_date)
        
        # sum top_up by agent
        top_up_agents = self.__sum_agent_top_up(closing_date)
        
        # get bf amt
        q_bfs = AgentMovement.query(AgentMovement.movement_date == closing_date + timedelta(days=-1))
        bfs = q_bfs.fetch()
        
        # group bf by agent code
        bf_agents = {}
        for bf in bfs:
            bf_obj = {}
            bf_obj['agent_code'] = bf.agent_code
            bf_obj['bal_amt'] = bf.bal_amt
            bf_agents[bf.agent_id] = bf_obj
             
        # get agents
        q_agent = Agent.query()
        agents = q_agent.fetch()
        
        # sum to balance
        bals = {}
        for agent in agents:
            bal_obj = None
            if bals.has_key(agent.id):
                bal_obj = bals[agent.id]
            else:
                bal_obj = AgentMovementViewModel()
                bal_obj.agent_id = agent.id
                bal_obj.movement_date = closing_date
                bals[agent.id] = bal_obj
            
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
                top_up_obj = top_up_agents[agent.id]
                bal_obj.top_up_amt = top_up_obj['amt']
                
        # cal bal amt
        for agent_id in bals:
            bal_obj = bals[agent_id]
            bal_obj.cal_bal_amt()
                
        # delete balance
        mv_da = AgentMovementDataAccess()
        mv_da.delete(closing_date)
            
        # insert balance
        for agent_id in bals:
            bal_obj = bals[agent_id]
            mv_da.create(bal_obj)
    
    def __sum_agent_deposit(self, closing_date):
        # get deposit
        q2 = Deposit.query(Deposit.tran_date == closing_date)
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
                deposit_obj['deposit_date'] = deposit.deposit_date
                deposit_obj['amt'] = 0
                deposit_agents[deposit.agent_code] = deposit_obj
                
            deposit_obj['amt'] += deposit.amt
            
        return deposit_agents
    
    def __sum_agent_top_up(self, closing_date):
        # get topup
        q2 = TopUp.query(TopUp.tran_date == closing_date)
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
    
    
    def revert(self, closing_obj):
        try:
            # get closing
            q = Closing.query()
            closing = q.get()
            
            # verify lock
            if closing.audit_lock == False:
                raise Exception('You must lock the system before revert.')
            
            # delete balance
            q2 = AgentMovement.query(AgentMovement.movement_date >= closing.closing_date + timedelta(days=-1))
            q2 = q2.filter(AgentMovement.movement_date <= closing.closing_date)
            bals = q2.fetch()
            
            for bal in bals:
                bal.key.delete()
            
            # update
            closing_da = ClosingDataAccess()
            closing_da.revert()
            
        except Exception as ex:
            da = UserAuditTrailDataAccess()
            da.create(closing_obj.user_id, 'Closing', 'Fail. Error=%s' % str(ex))
            raise ex
        
        da = UserAuditTrailDataAccess()
        da.create(closing_obj.user_id, 'Closing', 'Ok.')