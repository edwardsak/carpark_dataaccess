from datalayer.models.models import Buy, TopUp
from sharelib.utils import DateTime

class SaleByDay():
    def get(self, date_from, date_to):
        return self.__get(date_from, date_to)
    
    def __get(self, date_from, date_to, date_format='%Y%m%d'):
        # get buy
        q_buy = Buy.query()
        
        if date_from:
            q_buy = q_buy.filter(Buy.tran_date >= date_from)
            
        if date_to:
            q_buy = q_buy.filter(Buy.tran_date <= date_to)
            
        q_buy = q_buy.filter(Buy.void==False)
        buys = q_buy.order(Buy.tran_date).fetch()
        
        # get top_up
        q_top_up = TopUp.query()
        
        if date_from:
            q_top_up = q_top_up.filter(TopUp.tran_date >= date_from)
            
        if date_to:
            q_top_up = q_top_up.filter(TopUp.tran_date <= date_to)
            
        q_top_up = q_top_up.filter(TopUp.void==False)
        top_ups = q_top_up.order(TopUp.tran_date).fetch()
        
        # sum amt
        sale_list = []
        sale_days = {}
        
        for buy in buys:
            key = "%s" % (buy.tran_date.strftime(date_format))
            
            sale = None
            if sale_days.has_key(key):
                sale = sale_days[key]
            else:
                sale = SaleViewModel()
                sale.tran_date = buy.tran_date
                sale_days[key] = sale
                sale_list.append(sale)
                
            sale.buy_sub_total += buy.sub_total
            sale.buy_comm_amt += buy.comm_amt
            sale.buy_amt += buy.amt
            
        for top_up in top_ups:
            key = "%s" % (top_up.tran_date.strftime(date_format))
            
            sale = None
            if sale_days.has_key(key):
                sale = sale_days[key]
            else:
                sale = SaleViewModel()
                sale.tran_date = top_up.tran_date
                sale_days[key] = sale
                sale_list.append(sale)
            
            sale.top_up_sub_total += top_up.sub_total
            sale.top_up_comm_amt += top_up.comm_amt
            sale.top_up_amt += top_up.amt
            
        # cal amt
        for sale in sale_list:
            sale.cal_sub_total()
            sale.cal_amt()
            
        return sale_list
    
class SaleByMonth():
    def get(self, date_from, date_to):
        date_from2 = DateTime.first_day_of_month(date_from)
        date_to2 = DateTime.last_day_of_month(date_to)
        
        return self.__get(date_from2, date_to2, '%Y%m')
                
class SaleViewModel():
    tran_date = None
    buy_sub_total = 0
    buy_comm_amt = 0
    buy_amt = 0
    top_up_sub_total = 0
    top_up_comm_amt = 0
    top_up_amt = 0
    sub_total = 0
    amt = 0
    
    def cal_sub_total(self):
        self.sub_total = self.buy_sub_total + self.top_up_sub_total
        
    def cal_amt(self):
        self.amt = self.buy_amt + self.top_up_amt