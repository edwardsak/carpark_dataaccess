from datalayer.viewmodels.viewmodels import UserViewModel, AgentViewModel
from datalayer.appservice.admin.user import UserAppService
from datalayer.appservice.admin.agent import AgentAppService
from datalayer.appservice.admin.account import AccountAppService
from datalayer.models.models import User, Agent

import webapp2

class Test(webapp2.RequestHandler):
    def get(self):
        self.create_user()
        self.update_user()
        self.user_login()
        
        self.create_agent()
        self.update_agent()
    
    def create_user(self):
        try:
            vm = UserViewModel()
            vm.code = '1'
            vm.name = '1'
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
            vm.name = '2'
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