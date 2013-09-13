from datalayer.appservice.base.basetran import BaseTranAppService
from datalayer.dataaccess.topup import TopUpDataAccess
from datalayer.dataaccess.agentaudittrail import AgentAuditTrailDataAccess

class TopUpAppService(BaseTranAppService):
    def create(self, vm):
        try:
            self.validate_tran_date(vm)
            self.validate_closing(vm)
            self.__validate_agent_code(vm)
            self.__validate_car_reg_no(vm)
            self.__validate_sub_total(vm)
            
            # calculate amt
            vm.cal_comm_amt()
            vm.cal_amt()
            
            da = TopUpDataAccess()
            da.create(vm)
            
        except Exception, ex:
            audit_da = AgentAuditTrailDataAccess()
            audit_da.create(vm.agent_code, 'Create Top Up', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = AgentAuditTrailDataAccess()
        audit_da.create(vm.agent_code, 'Create Top Up', 'Ok.')
        
    def __validate_agent_code(self, vm):
        if vm.agent_code == None or len(vm.agent_code) < 1:
            raise Exception("You must enter an Agent ID.")
        
    def __validate_car_reg_no(self, vm):
        if vm.car_reg_no == None or len(vm.car_reg_no) < 1:
            raise Exception("You must enter an Car Reg. No.")
        
    def __validate_sub_total(self, vm):
        if vm.sub_total <= 0:
            raise Exception("You must enter a valid Amount.")