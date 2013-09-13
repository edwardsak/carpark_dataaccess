from datalayer.appservice.admin.reports.sale import SaleByDay
from datalayer.appservice.admin.reports.chargesummary import ChargeSummaryByDay
from sharelib.utils import DateTime

class ProfitByDay():
    def get(self, date_from, date_to):
        return self.__get(date_from, date_to)
    
    def __get(self, date_from, date_to, date_format='%Y%m%d'):
        # get cost
        sale_app = SaleByDay()
        sales = sale_app.get(date_from, date_to)
        
        # get charge
        charge_app = ChargeSummaryByDay()
        charges = charge_app.get(date_from, date_to)
        
        # group
        profit_list = []
        profit_days = {}
        
        for sale in sales:
            key = "%s" % (sale.tran_date.strftime(date_format))
            
            profit = None
            if profit_days.has_key(key):
                profit = profit_days[key]
            else:
                profit = ProfitViewModel()
                profit.tran_date = sale.tran_date
                profit_days[key] = profit
                profit_list.append(profit)
                
            profit.top_up_comm_amt += sale.top_up_comm_amt
            
        for charge in charges:
            key = "%s" % (charge.tran_date.strftime(date_format))
            
            profit = None
            if profit_days.has_key(key):
                profit = profit_days[key]
            else:
                profit = ProfitViewModel()
                profit.tran_date = charge.tran_date
                profit_days[key] = profit
                profit_list.append(profit)
                
            profit.charge_sub_total += charge.sub_total
            profit.charge_comm_amt += charge.comm_amt
            
        # sort by date
        profit_list = sorted(profit_list, key=lambda profit: profit.tran_date)
        
        # cal amt
        for profit in profit_list:
            profit.cal_amt()
            
        return profit_list
    
class ProfitByMonth():
    def get(self, date_from, date_to):
        date_from2 = DateTime.first_day_of_month(date_from)
        date_to2 = DateTime.last_day_of_month(date_to)
        
        return self.__get(date_from2, date_to2, date_format='%Y%m')
                
class ProfitViewModel():
    tran_date = None
    buy_sub_total = 0
    buy_comm_amt=  0
    top_up_sub_total = 0
    top_up_comm_amt = 0
    charge_sub_total = 0
    charge_comm_amt = 0
    amt = 0
    
    def cal_amt(self):
        self.amt = round(self.charge_sub_total - self.charge_comm_amt - self.top_up_comm_amt, 2)