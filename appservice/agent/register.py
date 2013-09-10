from datalayer.dataaccess.register import RegisterDataAccess
from datalayer.dataaccess.agentaudittrail import AgentAuditTrailDataAccess
from datalayer.models.models import Closing, SystemSetting
from sharelib.utils import DateTime

class RegisterAppService():
    def create(self, vm):
        try:
            self.__validate_tran_date(vm)
            self.__validate_agent_code(vm)
            self.__validate_car_reg_no(vm)
            self.__validate_customer_ic(vm)
            self.__validate_customer_name(vm)
            self.__validate_tag_code(vm)
            
            # get tag sell price
            system_setting = SystemSetting.query().get()
            vm.sub_total = system_setting.tag_sell_price
        
            da = RegisterDataAccess()
            da.create(vm)
            
        except Exception, ex:
            audit_da = AgentAuditTrailDataAccess()
            audit_da.create(vm.agent_code, 'Create Register', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = AgentAuditTrailDataAccess()
        audit_da.create(vm.agent_code, 'Create Register', 'Ok.')
        
    def __validate_tran_date(self, vm):
        if vm.tran_date is None:
            raise Exception('You must enter a Transaction Date.')
        
        closing = Closing.query().get()
            
        if DateTime.date_diff('day', closing.closing_date, vm.tran_date) < 0:
            raise Exception('You cannot create/modify this transaction because already closed.')
            
    def __validate_agent_code(self, vm):
        if vm.agent_code == None or len(vm.agent_code) < 1:
            raise Exception("You must enter an Agent ID.")
        
    def __validate_car_reg_no(self, vm):
        if vm.car_reg_no == None or len(vm.car_reg_no) < 1:
            raise Exception("You must enter an Car Reg. No.")
        
    def __validate_customer_ic(self, vm):
        if vm.customer_ic == None or len(vm.customer_ic) < 1:
            raise Exception("You must enter an IC/PP No.")
        
    def __validate_customer_name(self, vm):
        if vm.customer_name == None or len(vm.customer_name) < 1:
            raise Exception("You must enter a Name.")
        
    def __validate_tag_code(self, vm):
        if vm.tag_code == None or len(vm.tag_code) < 1:
            raise Exception("You must enter an Tag No.")