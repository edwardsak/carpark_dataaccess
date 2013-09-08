from datalayer.models.models import Tran

class UserViewModel():
    code = ''
    name = ''
    pwd = ''
    old_pwd = ''
    level = 3
    active = True
    last_modified = ''
    user_code = ''
    
class AgentViewModel():
    code = ''
    name = ''
    pwd = ''
    old_pwd = ''
    address = ''
    tel = ''
    hp = ''
    email = ''
    account_type = 1
    comm_per = 0
    bal_amt = 0
    active = True
    last_modified = ''
    user_code = ''

class AttendantViewModel():
    code = ''
    name = ''
    pwd = ''
    old_pwd = ''
    active = True
    last_modified = ''
    user_code = ''
    
class CarViewModel():
    reg_no = ''
    name = ''
    ic = ''
    address = ''
    hp = ''
    email = ''
    bal_amt = 0
    
class TagViewModel():
    code = ''
    agent_code = ''
    car_reg_no = ''
    
class TranViewModel():
    tran_type = 0
    tran_code = ''
    tran_date = None
    seq = 0
    agent_code = ''
    car_reg_no = ''
    
class AgentMovementViewModel():
    agent_code = ''
    movement_date = None
    bf_amt = 0
    deposit_amt = 0
    top_up_amt = 0
    bal_amt = 0
    
    def cal_bal_amt(self):
        self.bal_amt = round(self.bf_amt + self.deposit_amt - self.top_up_amt, 2)
        
class BuyViewModel():
    # view editable
    tran_date = None
    agent_code = ''
    qty = 0
    unit_price = 0
    sub_total = 0
    comm_per = 0
    comm_amt = 0
    amt = 0
    payment_date = None
    payment_type = 0
    payment_ref_no = ''
    payment_file_name = ''
    payment_url = ''
    verified_by = ''
    verify_status = 0
    void = False
    remark = ''
    last_modified = ''
    user_code = ''
    
    # model editable
    tran_type = Tran.TRAN_TYPE_BUY
    tran_code = ''
    seq = 0
    agent = None
    
    def cal_sub_total(self):
        self.sub_total = round(self.qty * self.unit_price, 2)
        
    def cal_comm_amt(self):
        self.comm_amt = round(self.sub_total * self.comm_per / 100, 2)
        
    def cal_amt(self):
        self.amt = round(self.sub_total - self.comm_amt, 2)
        
class DepositViewModel():
    # view editable
    tran_date = None
    agent_code = ''
    amt = 0
    payment_date = None
    payment_type = 0
    payment_ref_no = ''
    payment_file_name = ''
    payment_url = ''
    verified_by = ''
    verify_status = 0
    void = False
    remark = ''
    last_modified = ''
    user_code = ''
    
    # model editable
    tran_type = Tran.TRAN_TYPE_DEPOSIT
    tran_code = ''
    seq = 0
    agent = None
    
class RegisterViewModel():
    # view editable
    tran_date = None
    agent_code = ''
    car_reg_no = ''
    car_name = ''
    car_ic = ''
    car_address = ''
    car_tel = ''
    car_hp = ''
    car_email = ''
    tag_code = ''
    void = False
    remark = ''
    last_modified = ''
    user_code = ''
    
    # model editable
    tran_type = Tran.TRAN_TYPE_REGISTER
    tran_code = ''
    seq = 0
    agent = None
    car = None
        
class TopUpViewModel():
    # view editable
    tran_date = None
    agent_code = ''
    car_reg_no = ''
    sub_total = 0
    comm_per = 0
    comm_amt = 0
    amt = 0
    void = False
    remark = ''
    last_modified = ''
    user_code = ''
    
    # model editable
    tran_type = Tran.TRAN_TYPE_TOP_UP
    tran_code = ''
    seq = 0
    agent = None
    
    def cal_comm_amt(self):
        self.comm_amt = round(self.sub_total * self.comm_per / 100, 2)
        
    def cal_amt(self):
        self.amt = round(self.sub_total - self.comm_amt, 2)
        
class ChargeViewModel():
    # view editable
    tran_date = None
    attendant_code = ''
    lot_no = ''
    car_reg_no = ''
    void = False
    remark = ''
    last_modified = ''
    user_code = ''
    
    # model editable
    tran_type = Tran.TRAN_TYPE_CHARGE
    tran_code = ''
    seq = 0
    attendant = None
    car = None
    start_time = None
    charge_time = None
    duration = 0
    sub_total = 0
    comm_per = 0
    comm_amt = 0
    amt = 0
    
    def idle_duration(self):
        td = self.charge_time - self.last_charge_time
        return td.total_seconds() / 3600
    
    def cal_duration(self):
        td = self.charge_time - self.start_time
        self.duration = td.total_seconds() / 3600
        
    def cal_sub_total(self):
        amt = 0
        duration = self.duration
        
        if duration >= 0:
            amt = 0.21
        
        duration -= 1
        if duration > 0:
            amt += (int(duration) + 1) * 0.42
            
        self.sub_total = amt
    
    def cal_comm_amt(self):
        self.comm_amt = round(self.sub_total * self.comm_per / 100, 2)
        
    def cal_amt(self):
        self.amt = round(self.sub_total - self.comm_amt, 2)