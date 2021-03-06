from datalayer.appservice.base.basetran import BaseTranAppService
from datalayer.dataaccess.buy import BuyDataAccess
from datalayer.dataaccess.agentaudittrail import AgentAuditTrailDataAccess
from datalayer.dataaccess.systemsetting import SystemSettingDataAccess

class BuyAppService(BaseTranAppService):
    def create(self, vm):
        try:
            self.validate_tran_date(vm)
            self.validate_closing(vm)
            self.__validate_agent_code(vm)
            self.__validate_qty(vm)
            self.__validate_payment_date(vm)
            self.__validate_payment_type(vm)
            self.__validate_payment_ref_no(vm)
            
            # get unit_price
            system_da = SystemSettingDataAccess()
            setting = system_da.get()
            vm.unit_price = setting.tag_sell_price
            
            # calculate amt
            vm.cal_sub_total()
            vm.cal_comm_amt()
            vm.cal_amt()
            
            da = BuyDataAccess()
            da.create(vm)
            
        except Exception, ex:
            audit_da = AgentAuditTrailDataAccess()
            audit_da.create(vm.agent_code, 'Create Buy', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = AgentAuditTrailDataAccess()
        audit_da.create(vm.agent_code, 'Create Buy', 'Ok.')
        
    def __validate_agent_code(self, vm):
        if vm.agent_code == None or len(vm.agent_code) < 1:
            raise Exception("You must enter an Agent ID.")
        
    def __validate_qty(self, vm):
        if vm.qty < 1:
            raise Exception("You must enter a valid Qty.")
    
    def __validate_payment_date(self, vm):
        if vm.payment_date is None:
            raise Exception('You must enter a Payment Date.')
        
    def __validate_payment_ref_no(self, vm):
        if vm.payment_ref_no is None or len(vm.payment_ref_no) < 1:
            raise Exception('You must enter a Payment Ref. No.')
        
    def __validate_payment_type(self, vm):
        if vm.payment_type < 1 or vm.payment_type > 2:
            raise Exception('You must enter a valid Payment Type.')