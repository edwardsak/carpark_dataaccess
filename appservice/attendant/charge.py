from datalayer.dataaccess.charge import ChargeDataAccess
from datalayer.dataaccess.attendantaudittrail import AttendantAuditTrailDataAccess
from datalayer.models.models import Closing, Charge, Attendant, SystemSetting
from sharelib.utils import DateTime

class ChargeAppService():
    def create(self, vm):
        try:
            vm.charge_time = DateTime.malaysia_now()
            
            self.__validate_tran_date(vm)
            self.__validate_attendant_code(vm)
            self.__validate_lot_no(vm)
            self.__validate_car_reg_no(vm)
            
            # get attendance comm
            attendant = Attendant.query(Attendant.code==vm.attendant_code).get()
            if attendant is None:
                raise Exception('Attendant not found.')
            
            vm.comm_per = attendant.comm_per
            
            # get system setting
            system_setting = SystemSetting.query().get()
            
            # save charge
            da = ChargeDataAccess()
            
            # get charge
            charge = Charge.query(
                                  Charge.lot_no==vm.lot_no, 
                                  Charge.car_reg_no==vm.car_reg_no,
                                  Charge.tran_date==vm.tran_date,
                                  Charge.ended==False
                                  ).get()
            
            if charge is None:
                # new charge
                vm.start_time = vm.charge_time
                vm.last_charge_time = None
            else:
                # continue old charge
                vm.tran_code = charge.tran_code
                vm.start_time = charge.start_time
                vm.last_charge_time = charge.last_charge_time
            
                # if idle duration > 2hrs, end this charge
                # and create a new charge
                if vm.idle_duration() > system_setting.reset_duration:
                    # end charge
                    da.end(vm)
                    
                    # create new charge
                    vm.tran_code = ''
                    vm.start_time = vm.start_time
                    vm.last_charge_time = None
            
            vm.cal_duration()
            vm.cal_sub_total()
            vm.cal_comm_amt()
            vm.cal_amt()
            
            if len(vm.tran_code) < 1:
                da.create(vm)
            else:
                da.update_charge(vm)
            
        except Exception, ex:
            audit_da = AttendantAuditTrailDataAccess()
            audit_da.create(vm.agent_code, 'Create Charge', 'Fail. Error=%s' % str(ex))
            raise ex
        
        audit_da = AttendantAuditTrailDataAccess()
        audit_da.create(vm.agent_code, 'Create Charge', 'Ok.')
        
    def __validate_tran_date(self, vm):
        if vm.tran_date is None:
            raise Exception('You must enter a Transaction Date.')
        
        closing = Closing.query().get()
            
        if DateTime.date_diff('day', closing.closing_date, vm.tran_date) < 0:
            raise Exception('You cannot create/modify this transaction because already closed.')
            
    def __validate_attendant_code(self, vm):
        if vm.attendant_code == None or len(vm.attendant_code) < 1:
            raise Exception("You must enter an Attendant ID.")
        
    def __validate_lot_no(self, vm):
        if vm.lot_no == None or len(vm.lot_no) < 1:
            raise Exception("You must enter an Parking Space No.")
        
    def __validate_car_reg_no(self, vm):
        if vm.car_reg_no == None or len(vm.car_reg_no) < 1:
            raise Exception("You must enter an Car Reg. No.")
        
    def __validate_charge_time(self, vm):
        if vm.charge_time is None:
            raise Exception('You must enter a Charge Time.')