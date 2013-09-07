from datalayer.viewmodels.viewmodels import UserViewModel, AgentViewModel, BuyViewModel, DepositViewModel, RegisterViewModel, TopUpViewModel
from datalayer.appservice.admin.user import UserAppService
from datalayer.appservice.admin.agent import AgentAppService
from datalayer.appservice.admin.account import AccountAppService
from datalayer.appservice.admin.systemsetting import SystemSettingAppService
from datalayer.appservice.admin.closing import ClosingAppService
from datalayer.appservice.agent.buy import BuyAppService
from datalayer.appservice.agent.deposit import DepositAppService
from datalayer.appservice.agent.register import RegisterAppService
from datalayer.appservice.agent.topup import TopUpAppService
from datalayer.models.models import User, Agent, SystemSetting, Closing
from sharelib.object import Object
from sharelib.utils import DateTime

import datetime

import webapp2

class Test(webapp2.RequestHandler):
    def get(self):
        self.create_system_setting()
        self.create_closing()
        
        self.create_user()
        self.update_user()
        self.user_login()
        
        self.create_agent()
        self.update_agent()
        
        self.create_buy()
        self.create_deposit()
        self.create_register()
        self.create_top_up()
    
    def create_user(self):
        try:
            vm = UserViewModel()
            vm.code = '1'
            vm.name = 'admin'
            vm.pwd = '1'
            vm.level = 1
            
            app_service = UserAppService()
            app_service.create(vm)
            
            self.response.write("create_user OK.")
            
        except Exception, ex:
            self.response.write("create_user failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def update_user(self):
        try:
            user = User.query(User.code=='1').get()
            
            vm = UserViewModel()
            vm.code = '1'
            vm.name = 'admin2'
            vm.level = 1
            vm.last_modified = user.last_modified
            
            app_service = UserAppService()
            app_service.update(vm)
            
            self.response.write("update_user OK.")
            
        except Exception, ex:
            self.response.write("update_user failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def user_login(self):
        try:
            vm = UserViewModel()
            vm.code = '1'
            vm.pwd = '1'
            
            app_service = AccountAppService()
            app_service.login(vm)
            
            self.response.write("user_login OK.")
        
        except Exception, ex:
            self.response.write("user_login failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def create_agent(self):
        try:
            vm = AgentViewModel()
            vm.code = '1'
            vm.name = '1'
            vm.pwd = '1'
            vm.account_type = 1
            vm.comm_per = 5
            
            app_service = AgentAppService()
            app_service.create(vm)
            
            self.response.write("create_agent OK.")
            
        except Exception, ex:
            self.response.write("create_agent failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def update_agent(self):
        try:
            data = Agent.query(Agent.code=='1').get()
            
            vm = AgentViewModel()
            vm.code = '1'
            vm.name = '2'
            vm.account_type = 1
            vm.comm_per = 5
            vm.last_modified = data.last_modified
            
            app_service = AgentAppService()
            app_service.update(vm)
            
            self.response.write("update_agent OK.")
            
        except Exception, ex:
            self.response.write("update_agent failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def create_system_setting(self):
        try:
            system_setting = SystemSetting.query().get()
            if system_setting:
                self.response.write("System Setting already exist.")
                self.response.write("<br />")
                return
            
            vm = Object()
            vm.tag_sell_price = 10
            
            app_service = SystemSettingAppService()
            app_service.create(vm)
            
            self.response.write("create_system_setting OK.")
            
        except Exception, ex:
            self.response.write("create_system_setting failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def create_closing(self):
        try:
            closing = Closing.query().get()
            if closing:
                self.response.write("closing already exist.")
                self.response.write("<br />")
                return
            
            vm = Object()
            vm.closing_date = DateTime.malaysia_today() - datetime.timedelta(days=1)
            
            app_service = ClosingAppService()
            app_service.create(vm)
            
            self.response.write("create_closing OK.")
            
        except Exception, ex:
            self.response.write("create_closing failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def create_buy(self):
        try:
            vm = BuyViewModel()
            vm.tran_date = DateTime.malaysia_today()
            vm.agent_code = '1'
            vm.qty = 10
            vm.unit_price = 10
            vm.comm_per = 5
            vm.cal_sub_total()
            vm.cal_comm_amt()
            vm.payment_date = vm.tran_date
            vm.payment_type = 1
            vm.payment_ref_no = '1'
            vm.cal_amt()
            
            app_service = BuyAppService()
            app_service.create(vm)
            
            self.response.write("create_buy OK.")
            
        except Exception, ex:
            self.response.write("create_buy failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def create_deposit(self):
        try:
            vm = DepositViewModel()
            vm.tran_date = DateTime.malaysia_today()
            vm.agent_code = '1'
            vm.amt = 100
            vm.payment_date = vm.tran_date
            vm.payment_type = 1
            vm.payment_ref_no = '2'
            
            app_service = DepositAppService()
            app_service.create(vm)
            
            self.response.write("create_deposit OK.")
            
        except Exception, ex:
            self.response.write("create_deposit failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def create_register(self):
        try:
            vm = RegisterViewModel()
            vm.tran_date = DateTime.malaysia_today()
            vm.agent_code = '1'
            vm.car_reg_no = 'WKG4952'
            vm.car_name = 'Edward'
            vm.car_ic = '1234'
            vm.car_address = 'TB'
            vm.car_tel = '1'
            vm.car_hp = '2'
            vm.car_email = '3'
            vm.tag_code = 'XYZ'
            
            app_service = RegisterAppService()
            app_service.create(vm)
            
            self.response.write("create_register OK.")
            
        except Exception, ex:
            self.response.write("create_register failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def create_top_up(self):
        try:
            vm = TopUpViewModel()
            vm.tran_date = DateTime.malaysia_today()
            vm.agent_code = '1'
            vm.car_reg_no = 'WKG4952'
            vm.sub_total = 20
            vm.comm_per = 5
            vm.cal_comm_amt()
            vm.cal_amt()
            
            app_service = TopUpAppService()
            app_service.create(vm)
            
            self.response.write("create_top_up OK.")
            
        except Exception, ex:
            self.response.write("create_top_up failed. %s" % str(ex))
        
        self.response.write("<br />")