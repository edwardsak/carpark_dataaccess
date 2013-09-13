from datalayer.models.models import Charge
from sharelib.utils import DateTime

class ChargeSummaryByDayAndAttendant():
    def get(self, date_from, date_to, attendant_code):
        return self.__get(date_from, date_to, attendant_code)
    
    def __get(self, date_from, date_to, attendant_code, date_format='%Y%m%d'):
        # get charge
        q = Charge.query()
        
        if date_from:
            q = q.filter(Charge.tran_date >= date_from)
            
        if date_to:
            q = q.filter(Charge.tran_date <= date_to)
            
        if attendant_code and len(attendant_code) > 0:
            q = q.filter(Charge.attendant_code==attendant_code)
            
        q = q.filter(Charge.void==False)
        charges = q.order(Charge.tran_date, Charge.attendant_code).fetch()
        
        # sum amt
        charge_attendants = []
        charge_attendant_codes = {}
        for charge in charges:
            key = "%s|%s" % (charge.tran_date.strftime(date_format), charge.attendant_code)
            
            charge_attendant = None
            if charge_attendant_codes.has_key(key):
                charge_attendant = charge_attendant_codes[key]
            else:
                charge_attendant = ChargeSummaryViewModel()
                charge_attendant.tran_date = charge.tran_date
                charge_attendant.attendant_code = charge.attendant_code
                charge_attendant_codes[key] = charge_attendant
                charge_attendants.append(charge_attendant)
            
            charge_attendant.sub_total += charge.sub_total
            charge_attendant.comm_amt += charge.comm_amt
            charge_attendant.amt += charge.amt
        
        return charge_attendants
    
class ChargeSummaryByMonthAndAttendant():
    def get(self, date_from, date_to, attendant_code):
        date_from2 = DateTime.first_day_of_month(date_from)
        date_to2 = DateTime.last_day_of_month(date_to)
        
        # get charge
        summary_by_day = ChargeSummaryByDayAndAttendant()
        return summary_by_day.__get(date_from2, date_to2, attendant_code, '%Y%m')

class ChargeSummaryByDay():
    def get(self, date_from, date_to):
        return self.__get(date_from, date_to)
    
    def __get(self, date_from, date_to, date_format='%Y%m%d'):
        # get charge
        q = Charge.query()
        
        if date_from:
            q = q.filter(Charge.tran_date >= date_from)
            
        if date_to:
            q = q.filter(Charge.tran_date <= date_to)
            
        q = q.filter(Charge.void==False)
        charges = q.order(Charge.tran_date).fetch()
        
        # sum amt
        charge_list = []
        charge_days = {}
        for charge in charges:
            key = "%s" % (charge.tran_date.strftime(date_format))
            
            charge_day = None
            if charge_days.has_key(key):
                charge_day = charge_days[key]
            else:
                charge_day = ChargeSummaryViewModel()
                charge_day.tran_date = charge.tran_date
                charge_days[key] = charge_day
                charge_list.append(charge_day)
            
            charge_day.sub_total += charge.sub_total
            charge_day.comm_amt += charge.comm_amt
            charge_day.amt += charge.amt
        
        return charge_list
    
class ChargeSummaryByMonth():
    def get(self, date_from, date_to):
        date_from2 = DateTime.first_day_of_month(date_from)
        date_to2 = DateTime.last_day_of_month(date_to)
        
        # get charge
        summary_by_day = ChargeSummaryByDay()
        return summary_by_day.__get(date_from2, date_to2, '%Y%m')
    
class ChargeSummaryViewModel():
    tran_date = None
    attendant_code = ''
    sub_total = 0
    comm_amt = 0
    amt = 0