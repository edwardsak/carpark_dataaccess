from datalayer.models.models import Tran, Register, TopUp, Charge, CarMovement

from datetime import timedelta

class Statement():
    def get(self, car_reg_no, tran_date):
        # get bf amt
        bal_amt = 0
        bal_start_date = None
        
        car_mv = CarMovement.query(CarMovement.movement_date <= tran_date - timedelta(days=1)
                                   ).order(-CarMovement.movement_date).get()
        
        if car_mv:
            bal_amt = car_mv.bal_amt
            bal_start_date = car_mv.movement_date + timedelta(days=1)
            
        # get trans
        trans = Tran.query(
                           Tran.tran_date >= bal_start_date,
                           Tran.car_reg_no==car_reg_no
                           ).order(Tran.tran_date, Tran.seq).fetch()
            
        registers = Register.query(
                                   Register.tran_date >= bal_start_date,
                                   Register.car_reg_no==car_reg_no,
                                   Charge.void==False,
                                   ).fetch()
                                   
        top_ups = TopUp.query(
                              TopUp.tran_date >= bal_start_date,
                              TopUp.car_reg_no==car_reg_no,
                              Charge.void==False,
                              ).fetch()
                                   
        charges = Charge.query(
                               Charge.tran_date >= bal_start_date,
                               Charge.car_reg_no==car_reg_no,
                               Charge.void==False,
                               ).fetch()
                                   
        # group tran by tran_code
        mix_tran_codes = {}
        for register in registers:
            mix_tran_codes[register.tran_code] = register
            
        for top_up in top_ups:
            mix_tran_codes[top_up.tran_code] = top_up
            
        for charge in charges:
            mix_tran_codes[charge.tran_code] = charge
            
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
            tran_vm.car_reg_no = tran.car_reg_no
            
            if mix_tran_codes.has_key(tran.tran_code):
                mix_tran = mix_tran_codes[tran.tran_code]
                
                if tran.tran_type == Tran.TRAN_TYPE_REGISTER:
                    tran_vm.description = 'Register'
                    tran_vm.db_amt = mix_tran.sub_total
                elif tran.tran_type == Tran.TRAN_TYPE_TOP_UP:
                    tran_vm.description = 'Top Up'
                    tran_vm.db_amt = mix_tran.sub_total
                elif tran.tran_type == Tran.TRAN_TYPE_CHARGE:
                    tran_vm.description = 'Charge'
                    tran_vm.cr_amt = mix_tran.sub_total
                    
            tran_vm.cal_bal_amt()
            bal_amt = tran_vm.bal_amt
            
            return_values.append(tran_vm)
                
        return return_values
                
class StatementViewModel():
    tran_date = None
    tran_code = ''
    tran_type = 0
    car_reg_no = ''
    description = ''
    bf_amt = 0
    db_amt = 0
    cr_amt = 0
    bal_amt = 0
    
    def cal_bal_amt(self):
        self.bal_amt = self.bf_amt + self.db_amt - self.cr_amt