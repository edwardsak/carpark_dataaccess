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
    
class TranViewModel():
    tran_type = 0
    tran_code = ''
    tran_date = None
    seq = 0
    
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
    tran_type = 1
    tran_code = ''
    tran_date = None
    seq = 0
    agent_code = ''
    agent = None
    qty = 0
    unit_price = 0
    sub_total = 0
    comm_per = 0
    comm_amt = 0
    amt = 0
    payment_date = None
    payment_type = 0
    payment_ref_no = ''
    verified_by = ''
    verify_status = 0
    void = False
    remark = ''
    last_modified = ''
    user_code = ''
    
    def cal_sub_total(self):
        self.sub_total = round(self.qty * self.unit_price, 2)
        
    def cal_comm_amt(self):
        self.comm_amt = round(self.sub_total * self.comm_per / 100, 2)
        
    def cal_amt(self):
        self.amt = round(self.sub_total - self.comm_amt, 2)
        
class DepositViewModel():
    tran_type = 2
    tran_code = ''
    tran_date = None
    seq = 0
    agent_code = ''
    agent = None
    amt = 0
    payment_date = None
    payment_type = 0
    payment_ref_no = ''
    verified_by = ''
    verify_status = 0
    void = False
    remark = ''
    last_modified = ''
    user_code = ''
    
class RegisterViewModel():
    tran_type = 3
    tran_code = ''
    tran_date = None
    seq = 0
    agent_code = ''
    agent = None
    car_reg_no = ''
    tag_no = ''
    void = False
    remark = ''
    last_modified = ''
    user_code = ''
        
class TopUpViewModel():
    tran_type = 4
    tran_code = ''
    tran_date = None
    seq = 0
    agent_code = ''
    agent = None
    car_reg_no = ''
    sub_total = 0
    comm_per = 0
    comm_amt = 0
    amt = 0
    void = False
    remark = ''
    last_modified = ''
    user_code = ''
    
    def cal_comm_amt(self):
        self.comm_amt = round(self.sub_total * self.comm_per / 100, 2)
        
    def cal_amt(self):
        self.amt = round(self.sub_total - self.comm_amt, 2)