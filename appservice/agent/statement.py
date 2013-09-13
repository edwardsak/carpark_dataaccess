from datalayer.models.models import Tran, Buy, Deposit, Register, TopUp, AgentMovement

from datetime import timedelta

class Statement():
    def get(self, agent_code, tran_date):
        # get bf amt
        bal_amt = 0
        bal_start_date = None
        
        agent_mv = AgentMovement.query(
                                     AgentMovement.movement_date <= tran_date - timedelta(days=1)
                                     ).order(-AgentMovement.movement_date).get()
        
        if agent_mv:
            bal_amt = agent_mv.bal_amt
            bal_start_date = agent_mv.movement_date + timedelta(days=1)
            
        # get trans
        trans = Tran.query(
                           Tran.tran_date >= bal_start_date,
                           Tran.agent_code==agent_code
                           ).order(Tran.tran_date, Tran.seq).fetch()
        
        buys = Buy.query(
                         Buy.tran_date >= bal_start_date,
                         Buy.agent_code==agent_code,
                         Buy.void==False,
                         ).fetch()
                               
        deposits = Deposit.query(
                               Deposit.tran_date >= bal_start_date,
                               Deposit.agent_code==agent_code,
                               Deposit.void==False,
                               ).fetch()
                               
        registers = Register.query(
                                   Register.tran_date >= bal_start_date,
                                   Register.agent_code==agent_code,
                                   Register.void==False,
                                   ).fetch()
                                   
        top_ups = TopUp.query(
                              TopUp.tran_date >= bal_start_date,
                              TopUp.agent_code==agent_code,
                              TopUp.void==False,
                              ).fetch()
                                   
        # group tran by tran_code
        mix_tran_codes = {}
        for buy in buys:
            mix_tran_codes[buy.tran_code] = buy
            
        for deposit in deposits:
            mix_tran_codes[deposit.tran_code] = deposit
            
        for register in registers:
            mix_tran_codes[register.tran_code] = register
            
        for top_up in top_ups:
            mix_tran_codes[top_up.tran_code] = top_up
            
        # ppl records
        return_values = []
        
        # bf
        tran_bf_vm = StatementViewModel()
        tran_bf_vm.tran_date = bal_start_date
        tran_bf_vm.description = "B/F"
        tran_bf_vm.bal_amt = bal_amt
        return_values.append(tran_bf_vm)
        
        for tran in trans:
            tran_vm = StatementViewModel()
            tran_vm.bf_amt = bal_amt
            tran_vm.tran_date = tran.tran_date
            tran_vm.tran_code = tran.tran_code
            tran_vm.tran_type = tran.tran_type
            tran_vm.agent_code = tran.agent_code
            
            if mix_tran_codes.has_key(tran.tran_code):
                mix_tran = mix_tran_codes[tran.tran_code]
                
                if tran.tran_type == Tran.TRAN_TYPE_BUY:
                    tran_vm.description = 'Buy %s Tag(s)' % (mix_tran.qty)
                elif tran.tran_type == Tran.TRAN_TYPE_DEPOSIT:
                    tran_vm.description = 'Deposit'
                    tran_vm.db_amt = mix_tran.amt
                elif tran.tran_type == Tran.TRAN_TYPE_REGISTER:
                    tran_vm.description = "Register Car Reg. No. '%s'" % (mix_tran.car_reg_no)
                elif tran.tran_type == Tran.TRAN_TYPE_TOP_UP:
                    tran_vm.description = "Top Up Car Reg. No. '%s'" % (mix_tran.car_reg_no)
                    tran_vm.cr_amt = mix_tran.amt
                    
            tran_vm.cal_bal_amt()
            bal_amt = tran_vm.bal_amt
            
            return_values.append(tran_vm)
                
        return return_values
                
class StatementViewModel():
    tran_date = None
    tran_code = ''
    tran_type = 0
    agent_code = ''
    description = ''
    bf_amt = 0
    db_amt = 0
    cr_amt = 0
    bal_amt = 0
    
    def cal_bal_amt(self):
        self.bal_amt = round(self.bf_amt + self.db_amt - self.cr_amt, 2)