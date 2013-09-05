from datalayer.dataaccess.topup import TopUpDataAccess
from datalayer.dataaccess.agentaudittrail import AgentAuditTrailDataAccess
from datalayer.models.models import Closing
from sharelib.utils import DateTime

class TopUpAppService():
    def create(self, vm):
        try:
            self.__validate_tran_date(vm)
            self.__validate_agent_code(vm)
            self.__validate_car_reg_no(vm)
            self.__validate_amt(vm)
            
            da = TopUpDataAccess()
            da.create(vm)
            
        except Exception, ex:
            audit_da = AgentAuditTrailDataAccess()
            audit_da.create(vm.agent_code, 'Create Top Up', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = AgentAuditTrailDataAccess()
        audit_da.create(vm.agent_code, 'Create Top Up', 'Ok.')
        
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
        
    def __validate_amt(self, vm):
        if vm.amt < 1:
            raise Exception("You must enter a valid Amount.")