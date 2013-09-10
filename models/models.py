from google.appengine.ext import ndb

class UserAuditTrail(ndb.Model):
    user_code = ndb.StringProperty(required=True)
    action = ndb.StringProperty()
    message = ndb.StringProperty()
    
class AgentAuditTrail(ndb.Model):
    agent_code = ndb.StringProperty(required=True)
    action = ndb.StringProperty()
    message = ndb.StringProperty()
    
class AttendantAuditTrail(ndb.Model):
    attendant_code = ndb.StringProperty(required=True)
    action = ndb.StringProperty()
    message = ndb.StringProperty()
    
class CustomerAuditTrail(ndb.Model):
    ic = ndb.StringProperty(required=True)
    action = ndb.StringProperty()
    message = ndb.StringProperty()
    
class User(ndb.Model):
    code = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    pwd = ndb.StringProperty()
    level = ndb.IntegerProperty()
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()
    
    def get_level(self):
        return (1, 'Administrator'), (2, 'Super User'), (3, 'Limited User'), (4, 'Manager'), (5, 'Accountant')
    
class Agent(ndb.Model):
    code = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    pwd = ndb.StringProperty()
    address = ndb.StringProperty()
    tel = ndb.StringProperty()
    hp = ndb.StringProperty()
    email = ndb.StringProperty()
    account_type = ndb.IntegerProperty()
    comm_per = ndb.FloatProperty()
    bal_amt = ndb.FloatProperty()
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()
    
    def get_account_type(self):
        return (1, 'Normal'), (2, 'Corporate')
    
    def get_default_comm_per(self, account_type):
        if account_type == 1:
            return 5
        elif account_type == 2:
            return 8
        else:
            return 0
    
class Attendant(ndb.Model):
    code = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    pwd = ndb.StringProperty()
    comm_per = ndb.FloatProperty()
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()
    
class Customer(ndb.Model):
    ic = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    address = ndb.StringProperty()
    tel = ndb.StringProperty()
    hp = ndb.StringProperty()
    email = ndb.StringProperty()
    pwd = ndb.StringProperty()
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()
    
class Car(ndb.Model):
    reg_no = ndb.StringProperty(required=True)
    customer_ic = ndb.StringProperty()
    customer = ndb.KeyProperty(kind=Customer)
    bal_amt = ndb.FloatProperty()
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()
    
class Tag(ndb.Model):
    code = ndb.StringProperty(required=True)
    agent_code = ndb.StringProperty()
    agent = ndb.KeyProperty(kind=Agent)
    car_reg_no = ndb.StringProperty()
    car = ndb.KeyProperty(kind=Car)
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()

class Master(ndb.Model):
    kind = ndb.StringProperty(required=True)
    seq = ndb.IntegerProperty(required=True)
    
class Closing(ndb.Model):
    closing_date = ndb.DateTimeProperty()
    audit_lock = ndb.BooleanProperty()
    
class SystemSetting(ndb.Model):
    tag_sell_price = ndb.FloatProperty()
    reset_duration = ndb.FloatProperty()
    user_access_lock = ndb.BooleanProperty()
    agent_access_lock = ndb.BooleanProperty()
    attendant_access_lock = ndb.BooleanProperty()
    customer_access_lock = ndb.BooleanProperty()
    announcement = ndb.StringProperty()
       
class Tran(ndb.Model):
    tran_type = ndb.IntegerProperty(required=True)
    tran_code = ndb.StringProperty(required=True)
    tran_date = ndb.DateTimeProperty()
    seq = ndb.IntegerProperty()
    
    # to easy filter by agent and car reg no.
    agent_code = ndb.StringProperty()
    car_reg_no = ndb.StringProperty()
    
    TRAN_TYPE_BUY = 1
    TRAN_TYPE_DEPOSIT = 2
    TRAN_TYPE_REGISTER = 3
    TRAN_TYPE_TOP_UP = 4
    TRAN_TYPE_CHARGE = 5
    
    @staticmethod
    def get_tran_type():
        return (
                (Tran.TRAN_TYPE_BUY, 'Buy'), 
                (Tran.TRAN_TYPE_DEPOSIT, 'Deposit'), 
                (Tran.TRAN_TYPE_REGISTER, 'Register'), 
                (Tran.TRAN_TYPE_TOP_UP, 'Top Up'), 
                (Tran.TRAN_TYPE_CHARGE, 'Charge')
                )

class AgentMovement(ndb.Model):
    movement_code = ndb.StringProperty(required=True)
    agent_code = ndb.StringProperty(required=True)
    movement_date = ndb.DateTimeProperty(required=True)
    bf_amt = ndb.FloatProperty()
    deposit_amt = ndb.FloatProperty()
    top_up_amt = ndb.FloatProperty()
    bal_amt = ndb.FloatProperty()
    
    @staticmethod
    def get_movement_code(agent_code, movement_date):
        return "%s|%s" % (agent_code, movement_date.strftime('%Y%m%d'))
    
class CarMovement(ndb.Model):
    movement_code = ndb.StringProperty(required=True)
    car_reg_no = ndb.StringProperty(required=True)
    movement_date = ndb.DateTimeProperty(required=True)
    bf_amt = ndb.FloatProperty()
    register_amt = ndb.FloatProperty()
    top_up_amt = ndb.FloatProperty()
    charge_amt = ndb.FloatProperty()
    bal_amt = ndb.FloatProperty()
    
    @staticmethod
    def get_movement_code(car_reg_no, movement_date):
        return "%s|%s" % (car_reg_no, movement_date.strftime('%Y%m%d'))
    
class Receive(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    tran_type = ndb.IntegerProperty()
    tran_date = ndb.DateTimeProperty()
    seq = ndb.IntegerProperty()
    qty = ndb.IntegerProperty()
    unit_price = ndb.FloatProperty()
    amt = ndb.FloatProperty()
    created_by = ndb.StringProperty()
    created_date = ndb.DateTimeProperty()
    modified_by = ndb.StringProperty()
    modified_date = ndb.DateTimeProperty()
    void_by = ndb.StringProperty()
    void_date = ndb.DateTimeProperty()
    void = ndb.BooleanProperty()
    remark = ndb.StringProperty()
    last_modified = ndb.StringProperty()
    
class ReceiveDetail(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    seq = ndb.IntegerProperty()
    tag_code = ndb.StringProperty()
    tag = ndb.KeyProperty(kind=Tag)

class Deliver(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    tran_type = ndb.IntegerProperty()
    tran_date = ndb.DateTimeProperty()
    seq = ndb.IntegerProperty()
    qty = ndb.IntegerProperty()
    unit_price = ndb.FloatProperty()
    amt = ndb.FloatProperty()
    created_by = ndb.StringProperty()
    created_date = ndb.DateTimeProperty()
    modified_by = ndb.StringProperty()
    modified_date = ndb.DateTimeProperty()
    void_by = ndb.StringProperty()
    void_date = ndb.DateTimeProperty()
    void = ndb.BooleanProperty()
    remark = ndb.StringProperty()
    last_modified = ndb.StringProperty()
    
class DeliveryDetail(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    seq = ndb.IntegerProperty()
    tag_code = ndb.StringProperty()
    tag = ndb.KeyProperty(kind=Tag)
    
class Buy(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    tran_type = ndb.IntegerProperty()
    tran_date = ndb.DateTimeProperty()
    seq = ndb.IntegerProperty()
    agent_code = ndb.StringProperty(required=True)
    agent = ndb.KeyProperty(kind=Agent)
    qty = ndb.IntegerProperty()
    unit_price = ndb.FloatProperty()
    sub_total = ndb.FloatProperty()
    comm_per = ndb.FloatProperty()
    comm_amt = ndb.FloatProperty() 
    amt = ndb.FloatProperty()
    payment_date = ndb.DateTimeProperty()
    payment_type = ndb.IntegerProperty()
    payment_ref_no = ndb.StringProperty()
    payment_file_name = ndb.StringProperty()
    payment_url = ndb.StringProperty()
    verified_by = ndb.StringProperty()
    verify_status = ndb.IntegerProperty()
    created_by = ndb.StringProperty()
    created_date = ndb.DateTimeProperty()
    modified_by = ndb.StringProperty()
    modified_date = ndb.DateTimeProperty()
    void_by = ndb.StringProperty()
    void_date = ndb.DateTimeProperty()
    void = ndb.BooleanProperty()
    remark = ndb.StringProperty()
    last_modified = ndb.StringProperty()
    
    @staticmethod
    def get_tran_code(seq):
        return "BUY%04d" % seq
    
    @staticmethod
    def get_payment_type():
        return (1, 'Cash Bank In'), (2, 'Cheque Bank In')
    
    @staticmethod
    def get_verify_status():
        return (1, 'Accept'), (2, 'Reject')
    
class Deposit(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    tran_type = ndb.IntegerProperty()
    tran_date = ndb.DateTimeProperty()
    seq = ndb.IntegerProperty()
    agent_code = ndb.StringProperty(required=True)
    agent = ndb.KeyProperty(kind=Agent)
    amt = ndb.FloatProperty()
    payment_date = ndb.DateTimeProperty()
    payment_type = ndb.IntegerProperty()
    payment_ref_no = ndb.StringProperty()
    payment_file_name = ndb.StringProperty()
    payment_url = ndb.StringProperty()
    verified_by = ndb.StringProperty()
    verify_status = ndb.IntegerProperty()
    created_by = ndb.StringProperty()
    created_date = ndb.DateTimeProperty()
    modified_by = ndb.StringProperty()
    modified_date = ndb.DateTimeProperty()
    void_by = ndb.StringProperty()
    void_date = ndb.DateTimeProperty()
    void = ndb.BooleanProperty()
    remark = ndb.StringProperty()
    last_modified = ndb.StringProperty()
    
    @staticmethod
    def get_tran_code(seq):
        return "DEP%04d" % seq
    
class Register(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    tran_type = ndb.IntegerProperty()
    tran_date = ndb.DateTimeProperty()
    seq = ndb.IntegerProperty()
    agent_code = ndb.StringProperty(required=True)
    agent = ndb.KeyProperty(kind=Agent)
    car_reg_no = ndb.StringProperty(required=True)
    car = ndb.KeyProperty(kind=Car)
    customer_ic = ndb.StringProperty(required=True)
    customer_name = ndb.StringProperty(required=True)
    customer_address = ndb.StringProperty()
    customer_tel = ndb.StringProperty()
    customer_hp = ndb.StringProperty()
    customer_email = ndb.StringProperty()
    customer = ndb.KeyProperty(kind=Customer)
    tag_code = ndb.StringProperty(required=True)
    tag = ndb.KeyProperty(kind=Tag)
    sub_total = ndb.FloatProperty()
    created_by = ndb.StringProperty()
    created_date = ndb.DateTimeProperty()
    modified_by = ndb.StringProperty()
    modified_date = ndb.DateTimeProperty()
    void_by = ndb.StringProperty()
    void_date = ndb.DateTimeProperty()
    void = ndb.BooleanProperty()
    remark = ndb.StringProperty()
    last_modified = ndb.StringProperty()
    
    @staticmethod
    def get_tran_code(seq):
        return "REG%04d" % seq
    
class TopUp(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    tran_type = ndb.IntegerProperty()
    tran_date = ndb.DateTimeProperty()
    seq = ndb.IntegerProperty()
    agent_code = ndb.StringProperty(required=True)
    agent = ndb.KeyProperty(kind=Agent)
    car_reg_no = ndb.StringProperty(required=True)
    car = ndb.KeyProperty(kind=Car)
    sub_total = ndb.FloatProperty()
    comm_per = ndb.FloatProperty()
    comm_amt = ndb.FloatProperty()
    amt = ndb.FloatProperty()
    created_by = ndb.StringProperty()
    created_date = ndb.DateTimeProperty()
    modified_by = ndb.StringProperty()
    modified_date = ndb.DateTimeProperty()
    void_by = ndb.StringProperty()
    void_date = ndb.DateTimeProperty()
    void = ndb.BooleanProperty()
    remark = ndb.StringProperty()
    last_modified = ndb.StringProperty()
    
    @staticmethod
    def get_tran_code(seq):
        return "TOP%04d" % seq
    
class Charge(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    tran_type = ndb.IntegerProperty()
    tran_date = ndb.DateTimeProperty()
    seq = ndb.IntegerProperty()
    attendant_code = ndb.StringProperty(required=True)
    attendant = ndb.KeyProperty(kind=Attendant)
    car_reg_no = ndb.StringProperty(required=True)
    car = ndb.KeyProperty(kind=Car)
    lot_no = ndb.StringProperty()
    start_time = ndb.DateTimeProperty()
    charge_time = ndb.DateTimeProperty()
    duration = ndb.FloatProperty()
    sub_total = ndb.FloatProperty()
    comm_per = ndb.FloatProperty()
    comm_amt = ndb.FloatProperty()
    amt = ndb.FloatProperty()
    ended = ndb.BooleanProperty()
    created_by = ndb.StringProperty()
    created_date = ndb.DateTimeProperty()
    modified_by = ndb.StringProperty()
    modified_date = ndb.DateTimeProperty()
    void_by = ndb.StringProperty()
    void_date = ndb.DateTimeProperty()
    void = ndb.BooleanProperty()
    remark = ndb.StringProperty()
    last_modified = ndb.StringProperty()
    
    @staticmethod
    def get_tran_code(seq):
        return "CHR%04d" % seq