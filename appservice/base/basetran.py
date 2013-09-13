from datalayer.dataaccess.closing import ClosingDataAccess
from sharelib.utils import DateTime

class BaseTranAppService():
    def validate_tran_date(self, vm):
        if vm.tran_date is None:
            raise Exception('You must enter a Transaction Date.')
        
    def validate_closing(self, vm):
        closing_da = ClosingDataAccess()
        closing = closing_da.get()
        
        if closing.audit_lock:
            raise Exception("You cannot create/modify this transaction because already locked.")
            
        if DateTime.date_diff('day', closing.closing_date, vm.tran_date) < 0:
            raise Exception('You cannot create/modify this transaction because already closed.')