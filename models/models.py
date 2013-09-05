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
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()
    
class Customer(ndb.Model):
    ic = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    pwd = ndb.StringProperty()
    active = ndb.BooleanProperty()
    last_modified = ndb.StringProperty()
    
class Car(ndb.Model):
    reg_no = ndb.StringProperty(required=True)
    hp = ndb.StringProperty(required=True)
    
class Tag(ndb.Model):
    code = ndb.StringProperty(required=True)
    agent = ndb.KeyProperty(kind=Agent)
    car = ndb.KeyProperty(kind=Car)

class Master(ndb.Model):
    kind = ndb.StringProperty(required=True)
    seq = ndb.IntegerProperty(required=True)
    
class Closing(ndb.Model):
    closing_date = ndb.DateTimeProperty()
    
class SystemSetting(ndb.Model):
    tag_sell_price = ndb.FloatProperty()
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

class AgentMovement(ndb.Model):
    agent_code = ndb.StringProperty(required=True)
    movement_date = ndb.DateTimeProperty(required=True)
    bf_amt = ndb.FloatProperty()
    deposit_amt = ndb.FloatProperty()
    top_up_amt = ndb.FloatProperty()
    bal_amt = ndb.FloatProperty()
    
class Buy(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    tran_type = ndb.IntegerProperty()
    tran_date = ndb.DateTimeProperty()
    seq = ndb.IntegerProperty()
    agent_code = ndb.StringProperty()
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
    
    def get_tran_code(self):
        return "BUY%04d" % self.seq
    
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
    agent_code = ndb.StringProperty()
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
    
    def get_tran_code(self):
        return "DEP%04d" % self.seq
    
class Register(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    tran_type = ndb.IntegerProperty()
    tran_date = ndb.DateTimeProperty()
    seq = ndb.IntegerProperty()
    agent_code = ndb.StringProperty()
    agent = ndb.KeyProperty(kind=Agent)
    car_reg_no = ndb.StringProperty()
    tag_no = ndb.StringProperty()
    created_by = ndb.StringProperty()
    created_date = ndb.DateTimeProperty()
    modified_by = ndb.StringProperty()
    modified_date = ndb.DateTimeProperty()
    void_by = ndb.StringProperty()
    void_date = ndb.DateTimeProperty()
    void = ndb.BooleanProperty()
    remark = ndb.StringProperty()
    last_modified = ndb.StringProperty()
    
    def get_tran_code(self):
        return "REG%04d" % self.seq
    
class TopUp(ndb.Model):
    tran_code = ndb.StringProperty(required=True)
    tran_type = ndb.IntegerProperty()
    tran_date = ndb.DateTimeProperty()
    seq = ndb.IntegerProperty()
    agent_code = ndb.StringProperty()
    agent = ndb.KeyProperty(kind=Agent)
    car_reg_no = ndb.StringProperty()
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
    
    def get_tran_code(self):
        return "TOP%04d" % self.seq