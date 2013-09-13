from datalayer.viewmodels.viewmodels import SystemSettingViewModel, ClosingViewModel
from datalayer.viewmodels.viewmodels import UserViewModel, AgentViewModel, AttendantViewModel, CustomerViewModel
from datalayer.viewmodels.viewmodels import BuyViewModel, DepositViewModel, RegisterViewModel, TopUpViewModel, ChargeViewModel
from datalayer.appservice.admin.user import UserAppService
from datalayer.appservice.admin.agent import AgentAppService
from datalayer.appservice.admin.attendant import AttendantAppService
from datalayer.appservice.admin.customer import CustomerAppService
from datalayer.appservice.admin.account import AccountAppService as UserAccountAppService
from datalayer.appservice.admin.systemsetting import SystemSettingAppService
from datalayer.appservice.admin.closing import ClosingAppService
from datalayer.appservice.admin.reports.chargesummary import ChargeSummaryByDayAndAttendant, ChargeSummaryByDay
from datalayer.appservice.admin.reports.sale import SaleByDay
from datalayer.appservice.admin.reports.profit import ProfitByDay
from datalayer.appservice.agent.account import AccountAppService as AgentAccountAppService
from datalayer.appservice.agent.buy import BuyAppService
from datalayer.appservice.agent.deposit import DepositAppService
from datalayer.appservice.agent.register import RegisterAppService
from datalayer.appservice.agent.topup import TopUpAppService
from datalayer.appservice.agent.statement import Statement as AgentStatement
from datalayer.appservice.attendant.account import AccountAppService as AttendantAccountAppService
from datalayer.appservice.attendant.charge import ChargeAppService
from datalayer.appservice.customer.account import AccountAppService as CustomerAccountAppService
from datalayer.appservice.customer.statement import Statement as CarStatement
from datalayer.models.models import User, Agent, Attendant, Customer, SystemSetting, Closing
from sharelib.object import Object
from sharelib.utils import DateTime

import datetime

from google.appengine.ext import ndb
import webapp2

class Test(webapp2.RequestHandler):
    def get(self, case_no):
        if case_no == '1':
            self.test1()
        elif case_no == '2':
            self.test2()
        elif case_no == '3':
            self.test3()
        elif case_no == '4':
            self.test4()
        elif case_no == '5':
            self.test5()
        elif case_no == '6':
            self.test6()
        else:
            self.response.write("Test case not found.")
        
    def test1(self):
        self.create_system_setting()
        self.create_closing()
        
        self.create_user()
        self.update_user()
        self.user_login()
        
        self.create_agent()
        self.update_agent()
        self.agent_login()
        
        self.create_attendant()
        self.update_attendant()
        self.attendant_login()
        
        self.create_customer()
        self.update_customer()
        self.customer_login()
        
    def test2(self):
        self.create_buy()
        self.create_deposit()
        self.create_register()
        self.create_top_up()
        
    def test3(self):
        charge_time = DateTime.malaysia_now()
        self.create_charge()
        
        charge_time = charge_time + datetime.timedelta(minutes=61)
        self.create_charge(charge_time=charge_time)
        
        charge_time = charge_time + datetime.timedelta(minutes=61) 
        self.create_charge(charge_time=charge_time)
        
        charge_time = charge_time + datetime.timedelta(minutes=61)
        self.create_charge(charge_time=charge_time)
        
        charge_time = charge_time + datetime.timedelta(minutes=61)
        self.create_charge(charge_time=charge_time)
        
        charge_time = charge_time + datetime.timedelta(minutes=61)
        self.create_charge(charge_time=charge_time)
        
    def test4(self):
        self.closing_lock()
        self.closing_close()
        
    def test5(self):
        self.get_agent_statement()
        self.get_car_statement()
        
    def test6(self):
        self.get_charge_summary_by_day_and_attendant()
        self.get_charge_summary_by_day()
        self.get_sale_by_day()
        self.get_profit_by_day()
        
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
            user = User.query(ancestor=ndb.Key('User', '1')).get()
            
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
            
            app_service = UserAccountAppService()
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
            data = Agent.query(ancestor=ndb.Key('Agent', '1')).get()
            
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
        
    def agent_login(self):
        try:
            vm = AgentViewModel()
            vm.code = '1'
            vm.pwd = '1'
            
            app_service = AgentAccountAppService()
            app_service.login(vm)
            
            self.response.write("agent_login OK.")
        
        except Exception, ex:
            self.response.write("agent_login failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def create_attendant(self):
        try:
            vm = AttendantViewModel()
            vm.code = '1'
            vm.name = '1'
            vm.pwd = '1'
            vm.comm_per = 2
            
            app_service = AttendantAppService()
            app_service.create(vm)
            
            self.response.write("create_attendant OK.")
            
        except Exception, ex:
            self.response.write("create_attendant failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def update_attendant(self):
        try:
            data = Attendant.query(ancestor=ndb.Key('Attendant', '1')).get()
            
            vm = AttendantViewModel()
            vm.code = '1'
            vm.name = '2'
            vm.comm_per = 2
            vm.last_modified = data.last_modified
            
            app_service = AttendantAppService()
            app_service.update(vm)
            
            self.response.write("update_attendant OK.")
            
        except Exception, ex:
            self.response.write("update_attendant failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def attendant_login(self):
        try:
            vm = AttendantViewModel()
            vm.code = '1'
            vm.pwd = '1'
            
            app_service = AttendantAccountAppService()
            app_service.login(vm)
            
            self.response.write("attendant_login OK.")
        
        except Exception, ex:
            self.response.write("attendant_login failed. %s" % str(ex))
        
        self.response.write("<br />")
    
    def create_customer(self):
        try:
            vm = CustomerViewModel()
            vm.ic = '1'
            vm.name = '1'
            vm.address = '2'
            vm.tel = '3'
            vm.hp = '4'
            vm.email = '5'
            
            app_service = CustomerAppService()
            app_service.create(vm)
            
            self.response.write("create_customer OK.")
            
        except Exception, ex:
            self.response.write("create_customer failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def update_customer(self):
        try:
            data = Customer.query(ancestor=ndb.Key('Customer', '1')).get()
            
            vm = CustomerViewModel()
            vm.ic = '1'
            vm.name = '1'
            vm.address = 'a'
            vm.tel = '12'
            vm.hp = '13'
            vm.email = 'b'
            vm.last_modified = data.last_modified
            
            app_service = CustomerAppService()
            app_service.update(vm)
            
            self.response.write("update_customer OK.")
            
        except Exception, ex:
            self.response.write("update_customer failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def customer_login(self):
        try:
            vm = CustomerViewModel()
            vm.ic = '1'
            vm.pwd = '1'
            
            app_service = CustomerAccountAppService()
            app_service.login(vm)
            
            self.response.write("customer_login OK.")
        
        except Exception, ex:
            self.response.write("customer_login failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def create_system_setting(self):
        try:
            system_setting = SystemSetting.query().get()
            if system_setting:
                self.response.write("System Setting already exist.")
                self.response.write("<br />")
                return
            
            vm = SystemSettingViewModel()
            vm.tag_sell_price = 10
            vm.reset_duration = 2
            
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
            
            vm = ClosingViewModel()
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
            vm.customer_name = 'Edward'
            vm.customer_ic = '1'
            vm.customer_address = 'TB'
            vm.customer_tel = '1'
            vm.customer_hp = '2'
            vm.customer_email = '3'
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
        
    def create_charge(self, charge_time=None):
        try:
            vm = ChargeViewModel()
            vm.tran_date = DateTime.malaysia_today()
            vm.attendant_code = '1'
            vm.lot_no = '1'
            vm.car_reg_no = 'WKG4952'
            vm.comm_per = 2
            
            app_service = ChargeAppService()
            app_service.create(vm, charge_time)
            
            self.response.write("create_charge OK.")
            
        except Exception, ex:
            self.response.write("create_charge failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def closing_lock(self):
        try:
            vm = Object()
            vm.user_code = '1'
            
            app_service = ClosingAppService()
            app_service.lock(vm)
            
            self.response.write("closing_lock OK.")
            
        except Exception, ex:
            self.response.write("closing_lock failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def closing_close(self):
        try:
            vm = Object()
            vm.user_code = '1'
            
            app_service = ClosingAppService()
            app_service.close(vm)
            
            self.response.write("closing_close OK.")
            
        except Exception, ex:
            self.response.write("closing_close failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def get_agent_statement(self):
        try:
            statement = AgentStatement()
            values = statement.get('1', DateTime.malaysia_today())
            
            self.response.write("<table border='1'>")
            for value in values:
                self.response.write("<tr>")
                self.response.write("<td>%s</td>" % DateTime.to_date_string(value.tran_date))
                self.response.write("<td>%s</td>" % value.tran_code)
                self.response.write("<td>%s</td>" % value.description)
                self.response.write("<td>%s</td>" % value.db_amt)
                self.response.write("<td>%s</td>" % value.cr_amt)
                self.response.write("<td>%s</td>" % value.bal_amt)
                self.response.write("</tr>")
            self.response.write("</table>")
            
            self.response.write("get_agent_statement OK.")
        except Exception, ex:
            self.response.write("get_agent_statement failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def get_car_statement(self):
        try:
            statement = CarStatement()
            values = statement.get('WKG4952', DateTime.malaysia_today())
            
            self.response.write("<table border='1'>")
            for value in values:
                self.response.write("<tr>")
                self.response.write("<td>%s</td>" % DateTime.to_date_string(value.tran_date))
                self.response.write("<td>%s</td>" % value.tran_code)
                self.response.write("<td>%s</td>" % value.description)
                self.response.write("<td>%s</td>" % value.db_amt)
                self.response.write("<td>%s</td>" % value.cr_amt)
                self.response.write("<td>%s</td>" % value.bal_amt)
                self.response.write("</tr>")
            self.response.write("</table>")
            
            self.response.write("get_car_statement OK.")
        except Exception, ex:
            self.response.write("get_car_statement failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def get_charge_summary_by_day_and_attendant(self):
        try:
            charge_app = ChargeSummaryByDayAndAttendant()
            values = charge_app.get(DateTime.malaysia_today(), None, '')
            
            self.response.write("<table border='1'>")
            for value in values:
                self.response.write("<tr>")
                self.response.write("<td>%s</td>" % DateTime.to_date_string(value.tran_date))
                self.response.write("<td>%s</td>" % value.attendant_code)
                self.response.write("<td>%s</td>" % value.sub_total)
                self.response.write("<td>%s</td>" % value.comm_amt)
                self.response.write("<td>%s</td>" % value.amt)
                self.response.write("</tr>")
            self.response.write("</table>")
            
            self.response.write("get_charge_summary_by_day_and_attendant OK.")
        except Exception, ex:
            self.response.write("get_charge_summary_by_day_and_attendant failed. %s" % str(ex))
        
        self.response.write("<br />")
    
    def get_charge_summary_by_day(self):
        try:
            charge_app = ChargeSummaryByDay()
            values = charge_app.get(DateTime.malaysia_today(), None)
            
            self.response.write("<table border='1'>")
            for value in values:
                self.response.write("<tr>")
                self.response.write("<td>%s</td>" % DateTime.to_date_string(value.tran_date))
                self.response.write("<td>%s</td>" % value.sub_total)
                self.response.write("<td>%s</td>" % value.comm_amt)
                self.response.write("<td>%s</td>" % value.amt)
                self.response.write("</tr>")
            self.response.write("</table>")
            
            self.response.write("get_charge_summary_by_day OK.")
        except Exception, ex:
            self.response.write("get_charge_summary_by_day failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def get_sale_by_day(self):
        try:
            sale_app = SaleByDay()
            values = sale_app.get(DateTime.malaysia_today(), None)
            
            self.response.write("<table border='1'>")
            for value in values:
                self.response.write("<tr>")
                self.response.write("<td>%s</td>" % DateTime.to_date_string(value.tran_date))
                self.response.write("<td>%s</td>" % value.buy_sub_total)
                self.response.write("<td>%s</td>" % value.top_up_sub_total)
                self.response.write("<td>%s</td>" % value.sub_total)
                self.response.write("</tr>")
            self.response.write("</table>")
            
            self.response.write("get_sale_by_day OK.")
        except Exception, ex:
            self.response.write("get_sale_by_day failed. %s" % str(ex))
        
        self.response.write("<br />")
        
    def get_profit_by_day(self):
        try:
            profit_app = ProfitByDay()
            values = profit_app.get(DateTime.malaysia_today(), None)
            
            self.response.write("<table border='1'>")
            for value in values:
                self.response.write("<tr>")
                self.response.write("<td>%s</td>" % DateTime.to_date_string(value.tran_date))
                self.response.write("<td>%s</td>" % value.buy_sub_total)
                self.response.write("<td>%s</td>" % value.buy_comm_amt)
                self.response.write("<td>%s</td>" % value.top_up_sub_total)
                self.response.write("<td>%s</td>" % value.top_up_comm_amt)
                self.response.write("<td>%s</td>" % value.charge_comm_amt)
                self.response.write("<td>%s</td>" % value.amt)
                self.response.write("</tr>")
            self.response.write("</table>")
            
            self.response.write("get_profit_by_day OK.")
        except Exception, ex:
            self.response.write("get_profit_by_day failed. %s" % str(ex))
        
        self.response.write("<br />")